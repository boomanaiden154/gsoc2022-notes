set -e

processing_dir=./processing

test_suites=(
"blink_perf.accessibility"
"blink_perf.bindings"
"blink_perf.css"
"blink_perf.display_locking"
"blink_perf.dom"
"blink_perf.events"
"blink_perf.image_decoder"
"blink_perf.layout"
"blink_perf.layout_ng"
"blink_perf.owp_storage"
"blink_perf.paint"
"blink_perf.paint_layout_ng"
"blink_perf.parser"
"blink_perf.parser_layout_ng"
"blink_perf.sanitizer-api"
"blink_perf.shadow_dom"
"blink_perf.svg"
"blink_perf.webaudio"
"blink_perf.webcodecs"
"blink_perf.webgl_fast_call"
"blink_perf.webgl"
"blink_perf_xml_http_request.BlinkPerfXMLHttpRequest"
"octane"
"speedometer2"
"speedometer-future"
"speedometer"
)

if [ -d $processing_dir ]
then
	echo "$processing_dir already exists"
	exit
fi

mkdir $processing_dir

for test_suite in ${test_suites[@]}
do
	# current file is $1/results-$test_suite.html
	python3 extract_json.py $1/results-$test_suite.html > $processing_dir/${test_suite}_raw.json
	python3 process_json.py $processing_dir/${test_suite}_raw.json $processing_dir/${test_suite}_processed.json
	python3 process_test_suite.py $processing_dir/${test_suite}_processed.json $processing_dir/${test_suite}_processed_test_suite.json
	python3 compare_test_suites.py $processing_dir/${test_suite}_processed_test_suite.json $processing_dir/${test_suite}_compared.json
	echo ${test_suite} $(python3 results_summary.py $processing_dir/${test_suite}_compared.json)
done
