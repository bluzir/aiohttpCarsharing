import React from 'react';
import ReactDOM from 'react-dom';

var token = document.head.querySelector("[name=token]").content,
    ride = {};

var Ride = React.createClass({
  render: function() {
    return (
      <div className="ride__info">
         <h3>{ride.car.car_model}</h3>
      </div>
    );
  }
});

var App = React.createClass({
  render: function() {
    return (
      <div className="app">
        <ol className="breadcrumb">
          <li>Поездка:</li>
        </ol>
        <Ride data={ride}/>
      </div>
    );
  }
});

fetch('/api/ride/?token=' + token)
  .then(
    function(response) {
      response.json().then(function(data) {
        ride = data['rides'];
        ReactDOM.render(
            <div className="col-md-6"><App /></div>,
            document.getElementById('ride')
          );
      });
    }
  )
  .catch(function(err) {
    console.log('Fetch Error', err);
    return false;
});
