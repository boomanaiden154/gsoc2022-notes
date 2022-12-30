# Inlining Options in Clang/LLVM

Control over inlining can sometimes be useful when doing some things (like
evaluating cost models for register allocation). However, just keywords like
`inline` are sometimes not enough as the LLVM inliner only takes this as hints
and slightly adjusts the inlining threshold when that keyword is passed in
rather than actually just doing what the keyword would suggest. So first,
let's look at a motivating example:

```c
// The Computer Language Benchmarks Game
// https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
//
// Contributed by Mark C. Lewis.
// Modified slightly by Chad Whipkey.
// Converted from Java to C++ and added SSE support by Branimir Maksimovic.
// Converted from C++ to C by Alexey Medvedchikov.
// Modified by Jeremy Zerfas.

#include <stdint.h>
#include <stdalign.h>
#include <immintrin.h>
#include <math.h>
#include <stdio.h>

#ifdef CALL_COUNT_INSTRUMENTATION
static int64_t advanceCalls = 0;
static int64_t offset_MomentumCalls = 0;
static int64_t output_EnergyCalls = 0;
static int64_t mainCalls = 1;
#endif

// intptr_t should be the native integer type on most sane systems.
typedef intptr_t intnative_t;

typedef struct{
    double position[3], velocity[3], mass;
} body;

#define SOLAR_MASS (4*M_PI*M_PI)
#define DAYS_PER_YEAR 365.24
#define BODIES_COUNT 5

static body solar_Bodies[]={
    {    // Sun
        .mass=SOLAR_MASS
    },
    {    // Jupiter
        {
             4.84143144246472090e+00,
            -1.16032004402742839e+00,
            -1.03622044471123109e-01
        },
        {
             1.66007664274403694e-03 * DAYS_PER_YEAR,
             7.69901118419740425e-03 * DAYS_PER_YEAR,
            -6.90460016972063023e-05 * DAYS_PER_YEAR
        },
        9.54791938424326609e-04 * SOLAR_MASS
    },
    {    // Saturn
        {
             8.34336671824457987e+00,
             4.12479856412430479e+00,
            -4.03523417114321381e-01
        },
        {
            -2.76742510726862411e-03 * DAYS_PER_YEAR,
             4.99852801234917238e-03 * DAYS_PER_YEAR,
             2.30417297573763929e-05 * DAYS_PER_YEAR
        },
        2.85885980666130812e-04 * SOLAR_MASS
    },
    {    // Uranus
        {
             1.28943695621391310e+01,
            -1.51111514016986312e+01,
            -2.23307578892655734e-01
        },
        {
             2.96460137564761618e-03 * DAYS_PER_YEAR,
             2.37847173959480950e-03 * DAYS_PER_YEAR,
            -2.96589568540237556e-05 * DAYS_PER_YEAR
        },
        4.36624404335156298e-05 * SOLAR_MASS
    },
    {    // Neptune
        {
             1.53796971148509165e+01,
            -2.59193146099879641e+01,
             1.79258772950371181e-01
        },
        {
             2.68067772490389322e-03 * DAYS_PER_YEAR,
             1.62824170038242295e-03 * DAYS_PER_YEAR,
            -9.51592254519715870e-05 * DAYS_PER_YEAR
        },
        5.15138902046611451e-05 * SOLAR_MASS
    }
};


// Advance all the bodies in the system by one timestep. Calculate the
// interactions between all the bodies, update each body's velocity based on
// those interactions, and update each body's position by the distance it
// travels in a timestep at it's updated velocity.
#ifdef ALWAYS_INLINE
inline
#else
__attribute__((noinline))
#endif
static void advance(body bodies[], int bodiesCount) {
#ifdef CALL_COUNT_INSTRUMENTATION
    ++advanceCalls;
#endif
    // Figure out how many total different interactions there are between each
    // body and every other body. Some of the calculations for these
    // interactions will be calculated two at a time by using x86 SSE
    // instructions and because of that it will also be useful to have a
    // ROUNDED_INTERACTIONS_COUNT that is equal to the next highest even number
    // which is equal to or greater than INTERACTIONS_COUNT.
    int interactionsCount = (bodiesCount * (bodiesCount - 1) / 2);
    int roundedInteractionsCount = (interactionsCount + interactionsCount % 2);

    // It's useful to have two arrays to keep track of the position_Deltas
    // and magnitudes of force between the bodies for each interaction. For the
    // position_Deltas array, instead of using a one dimensional array of
    // structures that each contain the X, Y, and Z components for a position
    // delta, a two dimensional array is used instead which consists of three
    // arrays that each contain all of the X, Y, and Z components for all of the
    // position_Deltas. This allows for more efficient loading of this data into
    // SSE registers. Both of these arrays are also set to contain
    // ROUNDED_INTERACTIONS_COUNT elements to simplify one of the following
    // loops and to also keep the second and third arrays in position_Deltas
    // aligned properly.
    alignas(__m128d) double
      position_Deltas[3][roundedInteractionsCount],
      magnitudes[roundedInteractionsCount];

    // Calculate the position_Deltas between the bodies for each interaction.
    for(intnative_t i=0, k=0; i<bodiesCount-1; ++i)
        for(intnative_t j=i+1; j<bodiesCount; ++j, ++k)
            for(intnative_t m=0; m<3; ++m)
                position_Deltas[m][k]=
                  bodies[i].position[m]-bodies[j].position[m];

    // Calculate the magnitudes of force between the bodies for each
    // interaction. This loop processes two interactions at a time which is why
    // ROUNDED_INTERACTIONS_COUNT/2 iterations are done.
    for(intnative_t i=0; i<roundedInteractionsCount/2; ++i){

        // Load position_Deltas of two bodies into position_Delta.
        __m128d position_Delta[3];
        for(intnative_t m=0; m<3; ++m)
            position_Delta[m]=((__m128d *)position_Deltas[m])[i];

        const __m128d distance_Squared=
          position_Delta[0]*position_Delta[0]+
          position_Delta[1]*position_Delta[1]+
          position_Delta[2]*position_Delta[2];

        // Doing square roots normally using double precision floating point
        // math can be quite time consuming so SSE's much faster single
        // precision reciprocal square root approximation instruction is used as
        // a starting point instead. The precision isn't quite sufficient to get
        // acceptable results so two iterations of the Newton–Raphson method are
        // done to improve precision further.
        __m128d distance_Reciprocal=
          _mm_cvtps_pd(_mm_rsqrt_ps(_mm_cvtpd_ps(distance_Squared)));
        for(intnative_t j=0; j<2; ++j)
            // Normally the last four multiplications in this equation would
            // have to be done sequentially but by placing the last
            // multiplication in parentheses, a compiler can then schedule that
            // multiplication earlier.
            distance_Reciprocal=distance_Reciprocal*1.5-
              0.5*distance_Squared*distance_Reciprocal*
              (distance_Reciprocal*distance_Reciprocal);

        // Calculate the magnitudes of force between the bodies. Typically this
        // calculation would probably be done by using a division by the cube of
        // the distance (or similarly a multiplication by the cube of its
        // reciprocal) but for better performance on modern computers it often
        // will make sense to do part of the calculation using a division by the
        // distance_Squared which was already calculated earlier. Additionally
        // this method is probably a little more accurate due to less rounding
        // as well.
        ((__m128d *)magnitudes)[i]=0.01/distance_Squared*distance_Reciprocal;
    }

    // Use the calculated magnitudes of force to update the velocities for all
    // of the bodies.
    for(intnative_t i=0, k=0; i<bodiesCount-1; ++i)
        for(intnative_t j=i+1; j<bodiesCount; ++j, ++k){
            // Precompute the products of the mass and magnitude since it can be
            // reused a couple times.
            const double
              i_mass_magnitude=bodies[i].mass*magnitudes[k],
              j_mass_magnitude=bodies[j].mass*magnitudes[k];
            for(intnative_t m=0; m<3; ++m){
                bodies[i].velocity[m]-=position_Deltas[m][k]*j_mass_magnitude;
                bodies[j].velocity[m]+=position_Deltas[m][k]*i_mass_magnitude;
            }
        }

    // Use the updated velocities to update the positions for all of the bodies.
    for(intnative_t i=0; i<BODIES_COUNT; ++i)
        for(intnative_t m=0; m<3; ++m)
            bodies[i].position[m]+=0.01*bodies[i].velocity[m];
}


// Calculate the momentum of each body and conserve momentum of the system by
// adding to the Sun's velocity the appropriate opposite velocity needed in
// order to offset that body's momentum.
#ifdef ALWAYS_INLINE
inline
#else
__attribute__((noinline))
#endif
static void offset_Momentum(body bodies[]){
#ifdef CALL_COUNT_INSTRUMENTATION
    ++offset_MomentumCalls;
#endif
    for(intnative_t i=0; i<BODIES_COUNT; ++i)
        for(intnative_t m=0; m<3; ++m)
            bodies[0].velocity[m]-=
              bodies[i].velocity[m]*bodies[i].mass/SOLAR_MASS;
}


// Output the total energy of the system.
#ifdef ALWAYS_INLINE
inline
#else
__attribute__((noinline))
#endif
static void output_Energy(body bodies[]){
#ifdef CALL_COUNT_INSTRUMENTATION
    ++output_EnergyCalls;
#endif
    double energy=0;
    for(intnative_t i=0; i<BODIES_COUNT; ++i){

        // Add the kinetic energy for each body.
        energy+=0.5*bodies[i].mass*(
          bodies[i].velocity[0]*bodies[i].velocity[0]+
          bodies[i].velocity[1]*bodies[i].velocity[1]+
          bodies[i].velocity[2]*bodies[i].velocity[2]);

        // Add the potential energy between this body and every other body.
        for(intnative_t j=i+1; j<BODIES_COUNT; ++j){
            double position_Delta[3];
            for(intnative_t m=0; m<3; ++m)
                position_Delta[m]=bodies[i].position[m]-bodies[j].position[m];

            energy-=bodies[i].mass*bodies[j].mass/sqrt(
              position_Delta[0]*position_Delta[0]+
              position_Delta[1]*position_Delta[1]+
              position_Delta[2]*position_Delta[2]);
        }
    }

    // Output the total energy of the system.
#ifndef CALL_COUNT_INSTRUMENTATION
    printf("%.9f\n", energy);
#endif
}


int main(int argc, char *argv[]){
    offset_Momentum(solar_Bodies);
    output_Energy(solar_Bodies);
    for(intnative_t n=10000000; n--; advance(solar_Bodies, BODIES_COUNT));
    output_Energy(solar_Bodies);
#ifdef CALL_COUNT_INSTRUMENTATION
    printf("advance,%ld\n", advanceCalls);
    printf("offset_Momentum,%ld\n", offset_MomentumCalls);
    printf("output_Energy,%ld\n", output_EnergyCalls);
    printf("main,%ld\n", mainCalls);
#endif
}
```

This is one of the test programs that I'm playing around with to probe the
register allocation cost model (`/llvm/lib/CodeGen/RegAllocScore.cpp` in the
monorepo). I want to test if the model is breaking down significantly when
splitting things into multiple functions, but I don't want to rewrite it, so
inlining everything seems to be a good option. However, if we have clang
actually give us insight into the inlining process, we see the following:

```
clang /regalloc-testing/benchmarks/nbody.c -DALWAYS_INLINE -O3 -mllvm -debug-only=inline -o test
```

Results in the following output near the current tip of tree:

```
Using default inliner heuristic.
Inlining calls in: advance
    Function size: 137
    Size after inlining: 137
    Size after inlining: 137
    Size after inlining: 138
Updated inlining SCC: (advance)
Inlining calls in: main
    Function size: 11
Inlining calls in: main
    Function size: 11
    Inlining (cost=-14690, threshold=487), Call:   call fastcc void @offset_Momentum()
    Size after inlining: 78
    NOT Inlining (cost=975, threshold=974), Call:   call fastcc void @output_Energy()
    NOT Inlining (cost=975, threshold=974), Call:   call fastcc void @output_Energy()
    Inlining (cost=-12490, threshold=731), Call:   call fastcc void @advance(i32 noundef 5)
    Size after inlining: 669
Updated inlining SCC: (main)
```

It's inlining 2/3 functions, but it's not inlining `output_Energy()` even
though we annotated that function with the `inline` keyword. As we can see,
the inliner still thinks that the cost is above the threshold and doesn't inline.

Changing the `inline` keywords to function attributes (ie
`__attribute__((always_inline))` does result in inlining. But it can also be 
helpful to look at the flags to better control the inliner.
 [This](https://github.com/llvm/llvm-project/blob/6bb4b2d00221658b3fac421957e2905a13579c68/llvm/lib/Analysis/InlineCost.cpp)
file keeps most of the flags. The ones that we are interested in are `inline-threshold`
and `inlinehint-threshold`. Since the specific function that we want to inline
has a hint attached to it, we'll use `inlinehint-threshold` here. Using this
with clang:

```
clang /regalloc-testing/benchmarks/nbody.c -DALWAYS_INLINE -O3 -mllvm -debug-only=inline -mllvm -inlinehint-threshold=1000 -o test
```

Results in the following output:

```
Using default inliner heuristic.
Inlining calls in: advance
    Function size: 137
    Size after inlining: 137
    Size after inlining: 137
    Size after inlining: 138
Updated inlining SCC: (advance)
Inlining calls in: main
    Function size: 11
Inlining calls in: main
    Function size: 11
    Inlining (cost=-14690, threshold=1500), Call:   call fastcc void @offset_Momentum()
    Size after inlining: 78
    Inlining (cost=975, threshold=1500), Call:   call fastcc void @output_Energy()
    Size after inlining: 271
    Inlining (cost=-14025, threshold=1500), Call:   call fastcc void @output_Energy()
    Size after inlining: 464
    Inlining (cost=-12490, threshold=2250), Call:   call fastcc void @advance(i32 noundef 5)
    Size after inlining: 1055
Updated inlining SCC: (main)
```

And then just using `__attribute__(always_inline)` without adjusting the
threshold at all results in the following:

```
Using default inliner heuristic.
Inlining calls in: advance
    Function size: 137
    Size after inlining: 137
    Size after inlining: 137
    Size after inlining: 138
Updated inlining SCC: (advance)
Inlining calls in: main
    Function size: 11
    Size after inlining: 78
    Size after inlining: 271
    Size after inlining: 464
    Size after inlining: 1055
Updated inlining SCC: (main)
```