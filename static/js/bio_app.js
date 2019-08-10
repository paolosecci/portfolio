function buildMetadata(sample) {

  // @TODO: Complete the following function that builds the metadata panel
  console.log(sample);

  // Use `d3.json` to fetch the metadata for a sample
  var url = `/BioDiversity/metadata/${sample}`
  Plotly.d3.json(url, function(error, re){

    //log errors to console
    if(error) throw error;

    console.log("building metadata...");

    // Use d3 to select the panel with id of `#sample-metadata
    var $window = d3.select("#sample-metadata");

    // Use `.html("") to clear any existing metadata
    $window.html("");
    // Use `Object.entries` to add each key and value pair to the panel
    // Hint: Inside the loop, you will need to use d3 to append new
    // tags for each key-value in the metadata.

    var re_keys = Object.keys(re).map(this_key => this_key.toLowerCase());
    var re_vals = Object.values(re);
    console.log("keys: ", re_keys);
    console.log("values: ", re_vals);

    for(var i = 0; i < re_keys.length; i++)
    {
      $window.append('li')
          .html(`${re_keys[i]}: ${re_vals[i]}`);
    }
  });
    // BONUS: Build the Gauge Chart
    // buildGauge(data.WFREQ);
}

function buildCharts(sample) {

  // @TODO: Use `d3.json` to fetch the sample data for the plots
  var url = `/BioDiversity/samples/${sample}`
  Plotly.d3.json(url, function(error, re){

    if(error) throw error;
    console.log("re: ", re);

    // Build a Bubble Chart using the sample data
    console.log("building bubble chart...");

    var bubbleTrace = {
      type: "bubble",
      x: re.otu_ids,
      y: re.sample_values,
      mode: 'markers',
      marker: {
        size: re.sample_values,
        color: re.otu_ids
      },
      text: re.otu_labels
    };

    var bubbleLayout = {
      title: "Operational Taxonomic Unit (Weighted)"
    };

    Plotly.plot("bubble", [bubbleTrace], bubbleLayout);



    // @TODO: Build a Pie Chart
    // HINT: You will need to use slice() to grab the top 10 sample_values,
    // otu_ids, and labels (10 each).
    console.log("building pie chart...");

    //sort by sample_values
    sortable_arr = [];
    for(var i = 0; i < re.sample_values.length; i++)
    {
        temp_dict = {
          'samp_vals': re.sample_values[i],
          'ot_id': re.otu_ids[i],
          'ot_labs': re.otu_labels[i]
        }
        sortable_arr.push(temp_dict);
    }
    sortable_arr.sort((a, b) => (b.samp_vals - a.samp_vals));
    re2 = {
      'sv': [],
      'o_id': [],
      'o_labs': []
    }
    for(var i = 0; i < sortable_arr.length; i++)
    {
        re2.sv.push(sortable_arr[i].samp_vals);
        re2.o_id.push(sortable_arr[i].ot_id);
        re2.o_labs.push(sortable_arr[i].ot_labs);
    }
    console.log("re2: ", re2);



    //.slice(0,9);
    var pieTrace = {
      type: "pie",
      values: re2.sv.slice(0,9),
      labels: re2.o_id.slice(0,9),
      hovertext: re2.o_labs.slice(0,9)
    };

    var pieLayout = {
      title: `Biological Distribution of Sample`
    };

    Plotly.plot("pie", [pieTrace], pieLayout);

  });
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/BioDiversity/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();
