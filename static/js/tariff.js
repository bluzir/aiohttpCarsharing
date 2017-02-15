import React from 'react';
import ReactDOM from 'react-dom';

var token = document.head.querySelector("[name=token]").content,
    tariff = {};

var Tariff = React.createClass({
  render: function() {
    return (
      <div className="tariff__info">
         <h3><strong>Ваш тариф:</strong> {tariff.name}</h3>
      </div>
    );
  }
});

var App = React.createClass({
  render: function() {
    return (
      <div className="app">
        <ol className="breadcrumb">
          <li>Тариф</li>
        </ol>
        <Tariff data={tariff}/>
      </div>
    );
  }
});

fetch('/api/tariff/?token=' + token)
  .then(
    function(response) {
      response.json().then(function(data) {
        tariff = data['tariffs'];
        ReactDOM.render(
            <div className="col-md-6"><App /></div>,
            document.getElementById('tariff')
          );
      });
    }
  )
  .catch(function(err) {
    console.log('Fetch Error :-S', err);
    return false;
});
