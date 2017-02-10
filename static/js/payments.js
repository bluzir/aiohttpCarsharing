var token = document.head.querySelector("[name=token]").content,
    payments = {};

var Payments = React.createClass({
  render: function() {
    var data = this.props.data;
    var paymentsTemplate = data.map(function(item, index) {
      return (
        <a href={item.uuid+'/'}>
            <li key={index} className={item.payment > 0 ? 'list-group-item':'list-group-item list-group-item-danger'}>
                {item.summ} руб.
            </li>
        </a>
      )
    });

    return (
      <ul className="list-group">
        {paymentsTemplate}
      </ul>
    );
  }
});

var App = React.createClass({
  render: function() {
    return (
      <div className="app">
        <ol className="breadcrumb">
          <li><a className="active">Платежи</a></li>
        </ol>
        <div className="col-md-3">
        <Payments data={payments}/>
        </div>
      </div>
    );
  }
});

fetch('/api/payments/?token=' + token)
  .then(
    function(response) {
      response.json().then(function(data) {
        payments = data['invoices'];
        console.log(payments);
        ReactDOM.render(
            <App />,
            document.getElementById('payments')
          );
      });
    }
  )
  .catch(function(err) {
    console.log('Fetch Error :-S', err);
    return false;
});
