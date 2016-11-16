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
    var readingDivs = [];

    // Yes I know it would be better to use flexbox
    var grid = readings[i]['grid']

    var cells = grid.map(function(cell) {
      var pollution;

      if (cell < 30) {
        pollution = 'low';
      }
      else if (cell < 75) {
        pollution = 'mid';
      }
      else if (cell < 150) {
        pollution = 'high';
      }

      return (`
        <div class="grid-cell col" data-pollution=${pollution}></div>
      `)
    });

    final_ = `<div class="aq-reading" data-hour="${readings[i]['time']}">
        ${cells.join('\n')}
      </div>`

    $grid.append(final_);
  }

  $('.grid-cell').each(function() {
    colors = {'low': 'green', 'mid': 'orange', 'high': 'red'};
    p = this.dataset.pollution

    $(this).css('background-color', colors[p]);
  });

  cycle(readings, readings.length, 0);
}

function cycle(readings, num_hours, h) {
  $('.aq-reading').each(function() {
    try {
    if (this.dataset.hour === readings[h]['time']) {
      $(this).css('display', 'flex');
    }
    else $(this).css('display', 'none');
  }
    catch (e) {
      debugger
    }
  })

  // Loop the animation every half-second
  if (h < num_hours - 1) {
    $('#time').html(readings[h]['time'])
    setTimeout(cycle.bind(this, readings, num_hours, h+1), 400);
  }
  else {
    $('#time').html('Finished')
  }
}

getReadings();
