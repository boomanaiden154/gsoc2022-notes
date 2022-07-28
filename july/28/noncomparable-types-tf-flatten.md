# Multiple data types (eg tuples and strings) that aren't comparable when using tf.nest.flatten

Currently when making a call to `tf.nest.flatten` with a dictionary that has
multiple different key types that aren't comparable ends up resulting in an error
instead of a successful result. This is due to `tf.nest.flatten`'s internal use
of a sort function to make sure that results are deterministic. This is seen
in the classes `DictValueIterator` and `MappingValueIterator`
in `tensorflow/python/util/util.cc` in the main tensorflow repository. If this
was written in Python the solution would be quite easy as we could override the
key function of `list.sort()` to automatically return either the object passed to it
or the first element of a tuple. But this is implemented in the C API and currently
`PyList_Sort` doesn't support passing along a key function. Internally in CPython
`PyList_Sort` calls `list_sort_impl` which does implement allowing a key function,
but this function isn't currently exposed to the Public ABI with all of its parameters.
Maybe something to add to CPython at some point, but right now I need to get work done.