d3.json('/api/data').then(data => dashboard(data));
// css();

function css() {

  let element = d3.select('html').node();
  
  let width = element.getBoundingClientRect().width;

  let styles = getComputedStyle(document.querySelector(':root'));

  styles.setProperty('--width', width)

  console.log(styles.getPropertyValue('--width'))

};

function dashboard(data) {

  console.log(data);

  let total_words_frequencies = data.words.map(word => word['total_count']/data.total_words_count);

  console.log(total_words_frequencies);

  let wordhist = {
    x: total_words_frequencies,
    type: 'histogram'
  };

  let wordhistLayout = {
    title: 'Distribution of Word Frequencies',
    height: 500,
    width: 500,
    xaxis: {
      range: [0, .002],
      title: 'Word Frequency'
    },
    yaxis: {
      type: 'log',
      title: 'Log Number of Words'
    }
  };

  Plotly.newPlot('wordHist', [wordhist], wordhistLayout);

  let total_words_counts_by_document = data.documents.map(document => document['total_word_count']);

  let total_paragraphs_counts_by_document = data.documents.map(document => document['paragraphs_count']);

  console.log(total_words_counts_by_document);
  console.log(total_paragraphs_counts_by_document);

  let wordsPerParagragh = {
    type: 'scatter',
    mode: 'markers',
    x: total_paragraphs_counts_by_document,
    y: total_words_counts_by_document,
  };

  let wordsPerParagraghLayout = {
    title: 'Words Per Paragragh',
    height: 500,
    width: 500,
    xaxis: {title: 'Number of Paragraghs in  Document'},
    yaxis: {title: 'Total Number of Words in Document'}
  };

  Plotly.newPlot('wordsPerParagraph', [wordsPerParagragh], wordsPerParagraghLayout);

  let average_scrape_rate = data.documents_count/data.total_scrape_time*60;

  let scrapeRate = {
    domain: {x: [0, 1], y: [0, 1]},
    value: average_scrape_rate,
    type: "indicator",
    mode: "gauge+number",
    gauge: {
      axis: {
        range: [null, 10]
      }
    }
  };
    
  let scrapeRatelayout = {
    title: {
      text: "Srape Rate (Documents/Minute)"
    },
    width: 500,
    height: 500
  };

  Plotly.newPlot('scrapeRate', [scrapeRate], scrapeRatelayout);

  let locations = data.documents_with_location.map(document => [document.latitude, document.longitude, 1]);
  // let locations = random_locs(1000)

  documentMap = L.map('documentMap').setView([0, 0], 1);

  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19.,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(documentMap);

  let heat = L.heatLayer(locations, {
    max: 1,
    radius: 25,
    blur: 25,
    gradient: {0.4: 'blue', 1: 'red'}
  }).addTo(documentMap);

};

function random_locs(n) {
  let locs = [];
  for (i = 0; i < n; i ++) {
    locs.push([Math.random()*180-90, Math.random()*360-180]);
  };
  return locs;
}