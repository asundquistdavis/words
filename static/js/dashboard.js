// const used to control width of cards
let DIM = 450

// 
function drawWordHist(data) {
  // array containing word frequencies (total # word apears across all documents / total number of words across all documents)
  let total_words_frequencies = data.words.map(word => word['total_count']/data.total_words_count);
  // 
  let wordhist = {
    x: total_words_frequencies,
    type: 'histogram'
  };

  let wordhistLayout = {
    title: 'Distribution of Word Frequencies',
    height: DIM,
    width: DIM,
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
};

function drawWordsPerParagragh(data) {
  let total_words_counts_by_document = data.documents.map(document => document['total_word_count']);
  let total_paragraphs_counts_by_document = data.documents.map(document => document['paragraphs_count']);
  let wordsPerParagraphHT = data.documents.map(document => document['name']);

  let wordsPerParagragh = {
    type: 'scatter',
    mode: 'markers',
    x: total_paragraphs_counts_by_document,
    y: total_words_counts_by_document,
    text: wordsPerParagraphHT,
    hovertemplate: '<b>%{text}</b><br>Words: %{y}<br>Paragraphs: %{x}<extra></extra>'
  };

  let wordsPerParagraghLayout = {
    title: 'Words Per Paragragh',
    height: DIM,
    width: DIM,
    xaxis: {title: 'Number of Paragraghs in  Document'},
    yaxis: {title: 'Total Number of Words in Document'}
  };

  Plotly.newPlot('wordsPerParagraph', [wordsPerParagragh], wordsPerParagraghLayout);
};

function drawVowelFrequency(data) {

  let vowels = data.words.map(word=>word.vowel_count);
  let letters = data.words.map(word=>word.letter_count);
  let words = data.words.map(word=>word.word);

  let vowelFrequency = {
    type: 'scatter',
    mode: 'markers',
    x: vowels,
    y: letters,
    text: words,
    hovertemplate: '<b>%{text}</b><br>Letters: %{y}<br>Vowels: %{x}<extra></extra>'
  };

  let vowelFrequencyLayout = {
    title: 'Vowels vs Letters',
    height: DIM,
    width: DIM,
    xaxis: {title: 'Number of Vowels in Word'},
    yaxis: {title: 'Number of Letters in Word'}
  };

  Plotly.newPlot('vowelFrequency', [vowelFrequency], vowelFrequencyLayout);
};

function drawScrapeRate(data) {
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
    width: DIM,
    height: DIM
  };

  Plotly.newPlot('scrapeRate', [scrapeRate], scrapeRatelayout);
};

function drawDocumnentMap(data) {
  let locations = data.documents_with_location.map(document => [document.latitude, document.longitude, 1]);

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

async function dashboard() {

  let data = await d3.json('/api/data');
  drawWordHist(data);
  drawWordsPerParagragh(data);
  drawVowelFrequency(data);
  drawScrapeRate(data);
  drawDocumnentMap(data);

};

dashboard();