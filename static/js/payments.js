var token = document.head.querySelector("[name=token]").content,
    payments = {};


var Payments = React.createClass({
  render: function() {
    var data = this.props.data;
    var paymentsTemplate;

    if (data.length > 0) {
        paymentsTemplate = data.map(function(item, index) {
    return (
        <div key={index}>
            <Payment data={item} />
        </div>
    )
        })
    } else {
      paymentsTemplate = <p>Нет платежей</p>
    }

    return (
      <ul className="list-group">
        {paymentsTemplate}
      </ul>
    );
  }
});


var Payment = React.createClass({
    render: function () {
        var uuid = this.props.data.uuid,
            payment = this.props.data.payment,
            summ = this.props.data.summ;


        return (
            <a href={uuid+'/'}>
                <li
                    className={payment.status == 1 ? 'list-group-item list-group-item-success':'list-group-item list-group-item-danger'}>
                    {summ} руб.
                </li>
            </a>
      )
    }
});


var App = React.createClass({
  render: function() {
    return (
      <div className="app">
        <ol className="breadcrumb">
          <li>Платежи</li>
        </ol>
        <h3>Количество платежей: {payments.length} </h3>
        <div className="col-md-6">
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
            <div className="col-md-6"><App /></div>,
            document.getElementById('payments')
          );
      });
    }
  )
  .catch(function(err) {
    console.log('Fetch Error :-S', err);
    return false;
});
