$(document).ready(function() {
	$('[data-toggle=offcanvas]').click(function() {
		$('#main-row').toggleClass('active');
	});
});


$(document).ready(function() {
	ratingEl = $("#article-rating");
	ratingEl.css("display", "inline-block");
	ratingEl.width(Math.round(ratingEl.width() * (ratingEl.data("rating") / 5)));
});


// SEARCH AUTOCOMPLETION //
var SearchAutocomplete = function()
{
	var self = this;

	this.url = "/ajax/search/autocomplete/";
	this.minimumLength = 3;

	this.formElement = $(".search-autocomplete");
	this.queryBox = this.formElement.find("input[name=q]");

	// Watch the input box.
	this.queryBox.keyup(function()
	{
		if (this.value.length < self.minimumLength) {
			$(".autocomplete-results").remove();
			return false;
		}

		self.fetch(this.value);
	});

	// On selecting a result, populate the search field.
	this.formElement.on("click", ".autocomplete-result", function()
	{
		self.queryBox.val($(this).text());
		$(".autocomplete-results").remove();
		return false;
	});
}

SearchAutocomplete.prototype.fetch = function(query)
{
	var self = this;

	$.ajax({
		url: this.url,
		data: {
			"q": query
		},
		success: function(data) {
			self.showResults(data);
		}
	});
}

SearchAutocomplete.prototype.showResults = function(data)
{
	// Remove any existing results.
	$(".autocomplete-results").remove();

	var results = data.results || [];
	var resultsDropdown = $('<ul class="autocomplete-results dropdown-menu"></div>');
	var resultEntry = $('<li><a href="#" class="autocomplete-result"></a></li>');

	if (results.length > 0)
	{
		for (var offset in results)
		{
			var elem = resultEntry.clone();
			elem.find(".autocomplete-result").text(results[offset]);
			resultsDropdown.append(elem);
		}
	}
	else
	{
		resultsDropdown.append($('<li><p>No results found.</p></li>'));
	}

	this.queryBox.after(resultsDropdown);
}

$(document).ready(function()
{
	new SearchAutocomplete();
});
