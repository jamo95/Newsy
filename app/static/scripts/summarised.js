function switchSummarizerInput() {
  let showingText = $('#text-input').is(':visible');

  if (showingText) {
    setSummarizerInput('url');
  } else {
    setSummarizerInput('text');
  }

  $('#summarizer-title-input').val('');
  $('#summarizer-text-input').val('');
  $('#summarizer-url-input').val('');
}

function setSummarizerInput(to) {
  if (to === 'text') {
    $('#switch-input-link').text('Enter a URL instead');

    $('#text-input').show();
    $('#url-input').hide();

    window.location.hash = 'text';
  } else {
    $('#switch-input-link').text('Enter text instead');

    $('#url-input').show();
    $('#text-input').hide();

    window.location.hash = 'url';
  }
}
