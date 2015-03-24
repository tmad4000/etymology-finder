var cheerio = require('cheerio');
var request = require('request');
var fs = require('fs');
var _ = require('underscore');


var etymologyObj = {};

fs.readFile('wordsEn.txt', function(err, data) {
	if(err) throw err;
    var words = data.toString().split("\n");
    _.each(words, function(word) {
    request('http://en.wiktionary.org/wiki/' + word, function (error, response, html) {
      	if (!error && response.statusCode == 200) {
	      	var $ = cheerio.load(html);

	      	etymologyObj[word.replace('\r','')] = $('p').text();
	      	console.log(etymologyObj);

	    	fs.writeFile('etymology.json', 
	       	JSON.stringify(etymologyObj, null, 4));
    	}
	else {
		console.log('failed');
		}
	});
});
});
