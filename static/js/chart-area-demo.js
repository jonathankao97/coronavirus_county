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
var myLineChart
var myOtherLineChart
// Area Chart Example
function make_charts(slice, log=false, toggle_log=false){
if (slice==7){
    rad = 5;
} else if (slice==30){
    rad = 4;
} else if (slice==90){
    rad = 3;
}
beg = x_axis.length - Math.min(slice, x_axis.length)
if (myLineChart){
    myLineChart.destroy();
}
var canvas = document.getElementById("myAreaChart");
canvas.height=200;
console.log("here")
if(!log){
console.log("bye")
myLineChart = new Chart(canvas, {
  type: 'line',
  data: {
    labels: x_axis.slice(beg),
    datasets: [{
      label: "Confirmed",
      lineTension: 0,
      backgroundColor: "rgba(78, 115, 223, 0.05)",
      borderColor: "rgba(255, 255, 255, 0.8)",
      pointRadius: rad,
      pointBackgroundColor: "rgba(255, 255, 255, .8)",
      pointBorderColor: "rgba(255, 255, 255, 0)",
      pointHoverRadius: rad-1,
      pointHoverBackgroundColor: "rgba(255, 255, 255, .8)",
      pointHoverBorderColor: "rgba(255, 255, 255, 0)",
      pointHitRadius: 10,
      pointBorderWidth: 2,
      data: confirmed.slice(beg),
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
          fontFamily: "Helvetica"
        }
      }],
      yAxes: [{

        ticks: {
          precision: 0,
          padding: 20,
          min: 0,
         },
          // Include a dollar sign in the ticks
        gridLines: {
          color: "rgba(255, 255, 255, 0.4)",
          zeroLineColor: "rgba(255, 255, 255, 0.4)",
          drawBorder: false,
          borderDash: [2],
          zeroLineBorderDash: [2]
        },
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
} else {
console.log("hi")
myLineChart = new Chart(canvas, {
  type: 'line',
  data: {
    labels: x_axis.slice(beg),
    datasets: [{
      label: "Confirmed",
      lineTension: 0,
      backgroundColor: "rgba(78, 115, 223, 0.05)",
      borderColor: "rgba(255, 255, 255, 0.8)",
      pointRadius: rad,
      pointBackgroundColor: "rgba(255, 255, 255, .8)",
      pointBorderColor: "rgba(255, 255, 255, 0)",
      pointHoverRadius: rad-1,
      pointHoverBackgroundColor: "rgba(255, 255, 255, .8)",
      pointHoverBorderColor: "rgba(255, 255, 255, 0)",
      pointHitRadius: 10,
      pointBorderWidth: 2,
      data: confirmed.slice(beg),
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
          fontFamily: "Helvetica"
        }
      }],
      yAxes: [{
      type: 'logarithmic',
        ticks: {
          max: 1000000,
          padding: 20,
          min: 0,
           callback: function (value, index, values) {
             if (value === 1000000) return "1M";
             if (value === 100000) return "100K";
             if (value === 10000) return "10K";
             if (value === 1000) return "1K";
             if (value === 100) return "100";
             if (value === 10) return "10";
             if (value === 0) return "0";
             return null;
         }
         },
          // Include a dollar sign in the ticks
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
}
if(!toggle_log){
if (myOtherLineChart){
myOtherLineChart.destroy();
}
var canvas1 = document.getElementById("myDeathChart");
canvas1.height=200;
myOtherLineChart = new Chart(canvas1, {
 type: 'line',
  data: {
    labels: x_axis.slice(beg),
    datasets: [{
      label: "Deaths",
      lineTension: 0,
      backgroundColor: "rgba(78, 115, 223, 0.05)",
      borderColor: "rgba(255, 255, 255, 0.8)",
      pointRadius: rad,
      pointBackgroundColor: "rgba(255, 255, 255, .8)",
      pointBorderColor: "rgba(255, 255, 255, 0)",
      pointHoverRadius: rad-1,
      pointHoverBackgroundColor: "rgba(255, 255, 255, .8)",
      pointHoverBorderColor: "rgba(255, 255, 255, 0)",
      pointHitRadius: 10,
      pointBorderWidth: 2,
      data: deaths.slice(beg),
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
          fontFamily: "Helvetica"
        }
      }],
      yAxes: [{
        ticks: {
          maxTicksLimit: 5,
          padding: 20,
          min:0,
          precision: 0,
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
}

}

make_charts(7)