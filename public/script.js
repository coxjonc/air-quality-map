// DOM refs
var $grid = $('#overlay-grid'),
    $play = $('#fa-play'),
    $pause = $('#fa-pause'),
    $forward = $('#fa-forward'),
    $back = $('#fa-back');

// State
var paused = false;
    data = []; // Will hold all the grid data
    step = 0;

// Add event handlers for stepping forward and back
$pause.on('mousedown', function(e) {
  e.preventDefault();
  $pause.hide();
  $play.show();
  $forward.show();
  $back.show();
  paused = true;
})

$play.on('mousedown', function(e) {
  e.preventDefault();
  $(this).hide();
  $forward.hide();
  $back.hide();
  $pause.show();
  paused = false;
  cycle(step);
})

$forward.on('mousedown', function(e) {
  e.preventDefault();
  step += 1;
  cycle();
})

$back.on('mousedown', function(e) {
  e.preventDefault();
  step -= 1;
  cycle();
})

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
    rows = []
    for (var j=0; j<30; j++) {
      // Each reading contains a time and a list of 3 lists of intensities for grid cells
      var readingDivs = [];

      // Yes I know it would be better to use flexbox
      var grid = readings[i]['grid'];

      var cells = grid[j].map(function(cell) {
        var pollution;

        if (cell < 30) {
          pollution = 'low';
        }
        else if (cell < 70) {
          pollution = 'mid';
        }
        else {
          pollution = 'high';
        }

        return (`
          <div class="grid-cell" data-pollution=${pollution}></div>
        `)
      });
      rows.push(`<div class="row">${cells.join('\n')}</div>`);
    };

    final_ = `<div class="aq-reading" data-hour="${readings[i]['time']}">
        ${rows.join('\n')}
      </div>`

    $grid.append(final_);
  }

  $('.grid-cell').each(function() {
    colors = {'low': 'green', 'mid': 'orange', 'high': 'red'};
    p = this.dataset.pollution

    data = readings;
    $(this).css('background-color', colors[p]);
  });

  $('.aq-reading').each(function() {
    if (this.dataset.hour === data[step]['time']) {
      $(this).css('display', 'block');
    }
    else $(this).css('display', 'none');
  })
  step += 1;
  $('#time').html(data[0]['time'])

  $pause.hide();
  $play.show();
  $forward.show();
  $back.show();

  paused = true;
}

function cycle() {
  $('.aq-reading').each(function() {
    try {
    if (this.dataset.hour === data[step]['time']) {
      $(this).css('display', 'block');
    }
    else $(this).css('display', 'none');
  }
    catch (e) {
      debugger
    }
  })

  // Update the time
  $('#time').html(data[step]['time'])

  // Loop the animation every half-second
  if (step < data.length - 1 && !paused) {
    step += 1;
    setTimeout(cycle, 400);
  }
  else if (!paused){
    step = 0;
    setTimeout(cycle, 400);
  }
}

getReadings();
