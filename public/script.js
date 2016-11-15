// Dom refs
$grid = $('#overlay-grid');

function getReadings() {
  $.ajax({
    url: './aq_readings.json',
    dataType: 'json',
    success: function(res) {
      addGrid(res);
    }
  })
}

function addGrids(readings) {
  // readingDivs will hold the grids for each hourly report
  var readingDivs = [];

  // Loop through the reports for each hour since Nov 11
  for (var i=0; i<readings.length; i++) {
    // Each reading contains a time and a list of 3 lists of intensities for grid cells
    var readingDiv = [];

    // Yes I know it would be better to use flexbox
    for (var i=0; i<3; i++) {
      var row = readings[i]['grid'].map(function(cell) {
        return (`
          <div class="grid-cell" data-intensity=${cell}></div>
        `)
      });
      readingDiv.push(`div class="row">${row.join('\n')}</div>`);
    };

    freadingDiv = readingDiv.join('\n');
    readingDivs.push(`<div class="aq-reading" data-hour=${readings[i]['time']}>
      ${freadingDiv}
    </div>`);
  }
  // Append all the grids to the holder. Will display the correct one with cycle()
  $grid.html(readingDivs.join('\n'));
  cycle(0);
}

function cycle(h) {
  if (!readings) {
    console.log('No AQI readings loaded.')
  }
  else {
    $('.ag-reading').each(function() {
        if (this.dataset.hour === hours[h]) {
          $(this).show();
      }
      else $(this).hide();
    })

    // Loop the animation every half-second
    var next = (h === hours.length) ? -1 : h;
    setTimeout(cycle(next+1), 500);
  };
}

getReadings();
