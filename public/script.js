// DOM refs
$grid = $('#overlay-grid');

// Get the readings from a JSON file
function getReadings() {
  $.ajax({
    url: './aq_readings.json',
    dataType: 'json',
    success: function(res) {
      addGrids(res);
    }
  })
}

function addGrids(readings) {
  // readingDivs will hold the grids for each hourly report
  // Loop through the reports for each hour since Nov 11
  for (var i=0; i<readings.length; i++) {
    // Each reading contains a time and a list of 3 lists of intensities for grid cells
    var readingDiv = [];

    // Yes I know it would be better to use flexbox
    var grid = readings[i]['grid']
    for (var j=0; j<3; j++) {
      var row = grid[j].map(function(cell) {
        var pollution;

        if (cell < 50) {
          pollution = 'low';
        }
        else if (cell < 100) {
          pollution = 'mid';
        }
        else if (cell < 150) {
          pollution = 'high';
        }

        return (`
          <div class="grid-cell" data-pollution=${pollution}></div>
        `)
      });
      readingDiv.push(`<div class="row">${row.join('\n')}</div>`);
    };

    freadingDiv = readingDiv.join('\n');
    $grid.append(`<div class="aq-reading" data-hour=${readings[i]['time']}>
      ${freadingDiv}
    </div>`);
  }

  $('.grid-cell').each(function() {
    colors = {'low': 'green', 'mid': 'orange', 'high': 'red'};
    p = this.dataset.pollution

    $(this).css('background-color', colors[p]);
  });

  cycle(readings.length, 0);
}

function cycle(num_hours, h) {
  $('.aq-reading').each(function() {
      if (this.dataset.hour === hours[h]) {
        $(this).show();
    }
    else $(this).hide();
  })

  // Loop the animation every half-second
  if (h != 10) {
    setTimeout(cycle(num_hours, h+1), 500);
  }
}

getReadings();
