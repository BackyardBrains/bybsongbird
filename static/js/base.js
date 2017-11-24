$(function() {
    navbar_control();
    function navbar_control() {
        var current = location.pathname;
        $('.nav-link').each(function(){
            if($(this).attr('href') == current){
                $(this).addClass('active');
            }
        });
    }

    $('.nav-link').on('click', function() {
        $('.nav-link').each(function() {
            if ($(this).hasClass('active')) {
                console.log('has activate');
                $(this).removeClass('active');
            }
        });
        $(this).addClass('active');
    });
});

function donut_chart(data, color, chart, thischart) {
    var text = (data[0].value * 100).toFixed(3) + '%' ;
    var width = 90;
    var height = 90;
    var thickness = 10;

    var radius = Math.min(width, height) / 2;

    var svg = thischart.select("#" + chart)
        .append('svg')
        .attr('class', 'pie')
        .attr('width', width)
        .attr('height', height);

    var g = svg.append('g')
        .attr('transform', 'translate(' + (width/2) + ',' + (height/2) + ')');

    var arc = d3.arc()
        .innerRadius(radius - thickness)
        .outerRadius(radius);

    var pie = d3.pie()
        .value(function(d) { return d.value; })
        .sort(null);

    var path = g.selectAll('path')
        .data(pie(data))
        .enter()
        .append('path')
        .attr('d', arc)
        .attr('fill', (d, i) = > color[i];
)


        g.append('text')
            .attr('text-anchor', 'middle')
            .attr('dy', '.35em')
            .style("font-size", "14px")
            .text(text);
}

function show_map(sampleid, latitude, longitude, thismap) {
    var options = {
        zoom: 5,
        center: new google.maps.LatLng(44.182205, -84.506836), // Michigan
        mapTypeId: google.maps.MapTypeId.TERRAIN,
        mapTypeControl: false
    };

    var mapcanvas = new google.maps.Map(thismap[0], options);

    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(latitude, longitude),
        map: mapcanvas,
        title: 'Click Me'
    });

    google.maps.event.addListener(marker, 'click', function() {
        window.location.href = "/info?sampleid=" + sampleid;
    });

    marker.addListener('mouseover', function() {
        infowindow = new google.maps.InfoWindow({
            content: 'sampleid = ' + sampleid
        });
        infowindow.open(mapcanvas, marker);
    });

    marker.addListener('mouseout', function() {
        infowindow.close();
    });
}

function logout() {
    $.post('/api/logout').success(function () {
        window.location.reload(true);
    }).fail(function () {
        window.location.reload(true);
    })
}