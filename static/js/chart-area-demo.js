// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontColor = '#FFFFFF';

function number_format(number, decimals, dec_point, thousands_sep) {
  // *     example: number_format(1234.56, 2, ',', ' ');
  // *     return: '1 234,56'
  number = (number + '').replace(',', '').replace(' ', '');
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
    dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
    s = '',
    toFixedFix = function(n, prec) {
      var k = Math.pow(10, prec);
      return '' + Math.round(n * k) / k;
    };
  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || '';
    s[1] += new Array(prec - s[1].length + 1).join('0');
  }
  return s.join(dec);
}

// Area Chart Example
var ctx = document.getElementById("myAreaChart");
var ctx1 = document.getElementById("myDeathChart");
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: x_axis,
    datasets: [{
      label: "Cases",
      lineTension: 0,
      backgroundColor: "rgba(78, 115, 223, 0.05)",
      borderColor: "rgba(255, 255, 255, 0.8)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(255, 255, 255, .8)",
      pointBorderColor: "rgba(255, 255, 255, 0)",
      pointHoverRadius: 4,
      pointHoverBackgroundColor: "rgba(255, 255, 255, .8)",
      pointHoverBorderColor: "rgba(255, 255, 255, 0)",
      pointHitRadius: 10,
      pointBorderWidth: 2,
      data: confirmed,
    }],
  },
  options: {
    maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 5,
        bottom: 0
      }
    },
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 7,
          fontSize: 13,
          fontFamily: "Helvetica-light"
        }
      }],
      yAxes: [{
        ticks: {
          maxTicksLimit: 5,
          padding: 20,
          min: 380,
          // Include a dollar sign in the ticks
        },
        gridLines: {
          color: "rgba(255, 255, 255, 0.4)",
          zeroLineColor: "rgba(255, 255, 255, 0.4)",
          drawBorder: false,
          borderDash: [2],
          zeroLineBorderDash: [2]
        }
      }],
    },
    legend: {
      display: false
    },
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      intersect: false,
      mode: 'index',
      caretPadding: 10,
      callbacks: {
      }
    }
  }
});

var myOtherLineChart = new Chart(ctx1, {
 type: 'line',
  data: {
    labels: x_axis,
    datasets: [{
      label: "Deaths",
      lineTension: 0,
      backgroundColor: "rgba(78, 115, 223, 0.05)",
      borderColor: "rgba(255, 255, 255, 0.8)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(255, 255, 255, .8)",
      pointBorderColor: "rgba(255, 255, 255, 0)",
      pointHoverRadius: 4,
      pointHoverBackgroundColor: "rgba(255, 255, 255, .8)",
      pointHoverBorderColor: "rgba(255, 255, 255, 0)",
      pointHitRadius: 10,
      pointBorderWidth: 2,
      data: deaths,
    }],
  },
  options: {
    maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 5,
        bottom: 0
      }
    },
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 7,
          fontSize: 13,
          fontFamily: "Helvetica-light"
        }
      }],
      yAxes: [{
        ticks: {
          maxTicksLimit: 5,
          padding: 20,
          min: 0,
          // Include a dollar sign in the ticks
        },
        gridLines: {
          color: "rgba(255, 255, 255, 0.4)",
          zeroLineColor: "rgba(255, 255, 255, 0.4)",
          drawBorder: false,
          borderDash: [2],
          zeroLineBorderDash: [2]
        }
      }],
    },
    legend: {
      display: false
    },
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      intersect: false,
      mode: 'index',
      caretPadding: 10,
      callbacks: {
      }
    }
  }
});
