// Get csrtf token from html/view
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

function get_weather_data(){
    $.ajax({
        headers: { "X-CSRFToken": csrftoken },
        url: '',
        type: 'post',
        success: function(response){
            // console.log(response.weather_update)
            update_weather_data(response.weather_update);
        }
    });
}

function update_weather_data(cities){
    $('.media').each(function () { 
        city = $(this).find('.city').text()
        $(this).find('img').attr("src", "http://openweathermap.org/img/w/"+cities[city]['icon']+".png") 
        $(this).find('.temperature').text(cities[city]['temperature'])  
        $(this).find('.description').text(cities[city]['description']) 
    });
    
}

$(document).ready(function(){

    setInterval(get_weather_data,5000);

});