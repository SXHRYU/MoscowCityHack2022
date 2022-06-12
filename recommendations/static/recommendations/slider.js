$( function() {
    $( "#slider-range" ).slider({
      range: true,
      min: 6,
      max: 70,
      values: [ 6, 70 ],
      slide: function( event, ui ) {
        $( "#amount" ).val(ui.values[ 0 ] + " лет" + " - " + ui.values[ 1 ] + " лет");
      }
    });
    $( "#amount" ).val($( "#slider-range" ).slider( "values", 0 ) + " лет" + " - "
      + $( "#slider-range" ).slider( "values", 1 ) + " лет");
  } );