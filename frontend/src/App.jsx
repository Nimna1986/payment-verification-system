import { BrowserRouter, Routes, Route, Link, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "./services/api";
import "./App.css";

function Dashboard() {
  const [orders, setOrders] = useState([]);
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      api.get("/orders/"),
      api.get("/payments/")
    ])
      .then(([ordersResponse, paymentsResponse]) => {
        setOrders(ordersResponse.data);
        setPayments(paymentsResponse.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error(error);
        setError("Failed to load dashboard data.");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <h1>Loading dashboard...</h1>;
  }

  if (error) {
    return <h1>{error}</h1>;
  }

  const totalOrders = orders.length;

  const paidOrders = orders.filter(
    (order) => order.status === "PAID"
  ).length;

  const pendingOrders = orders.filter(
    (order) => order.status === "PENDING"
  ).length;

  const rejectedPayments = payments.filter(
    (payment) => payment.status === "rejected"
  ).length;

  return (
    <div className="container">
      <h1>Payment Verification Dashboard</h1>

      <div className="card-container">
        <div className="card">
          <h2>{totalOrders}</h2>
          <p>Total Orders</p>
        </div>

        <div className="card">
          <h2>{paidOrders}</h2>
          <p>Paid Orders</p>
        </div>

        <div className="card">
          <h2>{pendingOrders}</h2>
          <p>Pending Orders</p>
        </div>

        <div className="card">
          <h2>{rejectedPayments}</h2>
          <p>Rejected Payments</p>
        </div>
      </div>
    </div>
  );
}

function Orders() {
  const [orders, setOrders] = useState([]);
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [showPaymentForm, setShowPaymentForm] = useState(false);
  const [selectedOrder, setSelectedOrder] = useState(null);

  const [paymentAmount, setPaymentAmount] = useState("");
  const [paymentMethod, setPaymentMethod] = useState("LANKAPAY");
  const [transactionId, setTransactionId] = useState("");

  const [paymentLoading, setPaymentLoading] = useState(false);
  const [paymentError, setPaymentError] = useState("");

  const [showOrderForm, setShowOrderForm] = useState(false);

  const [customerName, setCustomerName] = useState("");
  const [expectedAmount, setExpectedAmount] = useState("");

  const [orderLoading, setOrderLoading] = useState(false);
  const [orderError, setOrderError] = useState("");

  const handleCreateOrder = async (event) => {
  event.preventDefault();

  if (!customerName || !expectedAmount) {
    setOrderError("Please fill in all fields.");
    return;
  }

  setOrderLoading(true);
  setOrderError("");

  try {
    const response = await api.post("/orders/", {
      customer_name: customerName,
      expected_amount: Number(expectedAmount)
    });

    setOrders((previousOrders) => [
      ...previousOrders,
      response.data
    ]);

    setCustomerName("");
    setExpectedAmount("");

    setShowOrderForm(false);
  } catch (error) {
    console.error(error);

    if (error.response) {
      setOrderError(
        error.response.data.detail ||
        "Failed to create order."
      );
    } else {
      setOrderError(
        "Could not connect to the backend."
      );
    }
  } finally {
    setOrderLoading(false);
  }
};

  useEffect(() => {
    Promise.all([
      api.get("/orders/"),
      api.get("/payments/")
    ])
      .then(([ordersResponse, paymentsResponse]) => {
        setOrders(ordersResponse.data);
        setPayments(paymentsResponse.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error(error);
        setError("Failed to load orders and payments.");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="container">
        <h1>Orders</h1>
        <p>Loading orders...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container">
        <h1>Orders</h1>
        <p>{error}</p>
      </div>
    );
  }
  const handleAddPayment = async (event) => {
  event.preventDefault();

  if (!selectedOrder) {
    return;
  }

  if (!paymentAmount || !transactionId) {
    setPaymentError(
      "Please enter the payment amount and transaction ID."
    );
    return;
  }

  setPaymentLoading(true);
  setPaymentError("");

  try {
    const response = await api.post("/payments/", {
      amount: Number(paymentAmount),
      payment_method: paymentMethod,
      transaction_id: transactionId,
      order_id: selectedOrder.id,
      status:"pending",
      user_id: 1
    });

    setPayments((previousPayments) => [
      ...previousPayments,
      response.data
    ]);

    setShowPaymentForm(false);

    setPaymentAmount("");
    setPaymentMethod("LANKAPAY");
    setTransactionId("");
    setSelectedOrder(null);
  } catch (error) {
    console.error(error);

    if (error.response) {
      setPaymentError(
        error.response.data.detail ||
        "Failed to create payment."
      );
    } else {
      setPaymentError(
        "Could not connect to the backend."
      );
    }
  } finally {
    setPaymentLoading(false);
  }
};

  return (
    <div className="container">
      <h1>Orders</h1>

      <button
      className="btn"
  onClick={() => {
    setShowOrderForm(true);
    setOrderError("");
  }}
>
  + Create Order
</button>
      <p>
        Total orders: <strong>{orders.length}</strong>
      </p>
      {showOrderForm && (
  <div className="order-form">
    <h2>Create Order</h2>

    <form onSubmit={handleCreateOrder}>

      <div>
        <label>Customer Name</label>
        <br />

        <input
          type="text"
          value={customerName}
          onChange={(event) =>
            setCustomerName(event.target.value)
          }
          placeholder="Customer name"
        />
      </div>

      <br />

      <div>
        <label>Expected Amount</label>
        <br />

        <input
          type="number"
          value={expectedAmount}
          onChange={(event) =>
            setExpectedAmount(event.target.value)
          }
          placeholder="35000"
        />
      </div>

      <br />

      {orderError && (
        <p>{orderError}</p>
      )}

      <button
        type="submit"
        disabled={orderLoading}
      >
        {orderLoading
          ? "Creating..."
          : "Create Order"}
      </button>

      {" "}

      <button
        type="button"
        onClick={() => {
          setShowOrderForm(false);
          setOrderError("");
        }}
      >
        Cancel
      </button>

    </form>
  </div>
)}

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Order Number</th>
            <th>Customer</th>
            <th>Expected Amount</th>
            <th>Payment</th>
            <th>Payment Amount</th>
            <th>Payment Status</th>
            <th>Order Status</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          {orders.map((order) => {
            const payment = payments.find(
              (payment) => payment.order_id === order.id
            );

            return (
              <tr key={order.id}>
                <td>{order.id}</td>

                <td>
                  <strong>{order.order_number}</strong>
                </td>

                <td>{order.customer_name}</td>

                <td>
                  LKR{" "}
                  {Number(order.expected_amount).toLocaleString()}
                </td>

                <td>
                  {payment ? (
                    <>Payment #{payment.id}</>
                  ) : (
                    "No Payment"
                  )}
                </td>

                <td>
                  {payment ? (
                    `LKR ${Number(payment.amount).toLocaleString()}`
                  ) : (
                    "-"
                  )}
                </td>

                <td>
                  {payment ? (
                    <span
                      className={`status ${payment.status.toLowerCase()}`}
                    >
                      {payment.status.toUpperCase()}
                    </span>
                  ) : (
                    "-"
                  )}
                </td>
                

                <td>
                  <span
                    className={`status ${order.status.toLowerCase()}`}
                  >
                    {order.status}
                  </span>
                </td>
                <td>
                  {payment ? (
                    payment.status.toLowerCase() === "pending" ? (
                      <Link to={`/verify-payment/${payment.id}`}>
                        <p className="verifybtn">Verify Payment</p>
                      </Link>
                    ) : (
                      "-"
                    )
                  ) : (
                    <button
                      onClick={() => {
                        setSelectedOrder(order);
                        setPaymentAmount(order.expected_amount);
                        setShowPaymentForm(true);
                        setPaymentError("");
                      }}
                    >
                      Add Payment
                    </button>
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>

      {showPaymentForm && selectedOrder && (
  <div className="payment-form">
    <h2>Add Payment</h2>

    <p>
      <strong>Order:</strong>{" "}
      {selectedOrder.order_number}
    </p>

    <p>
      <strong>Customer:</strong>{" "}
      {selectedOrder.customer_name}
    </p>

    <p>
      <strong>Expected Amount:</strong>{" "}
      LKR{" "}
      {Number(
        selectedOrder.expected_amount
      ).toLocaleString()}
    </p>

    <form onSubmit={handleAddPayment}>

      <div>
        <label>Payment Amount</label>
        <br />

        <input
          type="number"
          value={paymentAmount}
          onChange={(event) =>
            setPaymentAmount(event.target.value)
          }
        />
      </div>

      <br />

      <div>
        <label>Payment Method</label>
        <br />

        <select
          value={paymentMethod}
          onChange={(event) =>
            setPaymentMethod(event.target.value)
          }
        >
          <option value="LANKAPAY">
            LANKAPAY
          </option>

          <option value="BANK_TRANSFER">
            BANK_TRANSFER
          </option>
        </select>
      </div>

      <br />

      <div>
        <label>Transaction ID</label>
        <br />

        <input
          type="text"
          value={transactionId}
          onChange={(event) =>
            setTransactionId(event.target.value)
          }
          placeholder="Enter transaction ID"
        />
      </div>

      <br />

      {paymentError && (
        <p>
          {paymentError}
        </p>
      )}

      <button
        type="submit"
        disabled={paymentLoading}
      >
        {paymentLoading
          ? "Creating Payment..."
          : "Create Payment"}
      </button>

      {" "}

      <button
        type="button"
        onClick={() => {
          setShowPaymentForm(false);
          setSelectedOrder(null);
          setPaymentError("");
        }}
      >
        Cancel
      </button>

    </form>
  </div>
)}

      {orders.length === 0 && (
        <p>No orders found.</p>
      )}
    </div>
  );
}

function VerifyPayment() {
  const { paymentId: urlPaymentId } = useParams();

  const [paymentId, setPaymentId] = useState(urlPaymentId || "");
  const [payment, setPayment] = useState(null);
  const [order, setOrder] = useState(null);

  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const amountMatches =
  payment &&
  order &&
  Number(payment.amount) === Number(order.expected_amount);

  useEffect(() => {
    if (!urlPaymentId) {
      return;
    }

    Promise.all([
      api.get("/payments/"),
      api.get("/orders/")
    ])
      .then(([paymentsResponse, ordersResponse]) => {
        const foundPayment = paymentsResponse.data.find(
          (payment) => payment.id === Number(urlPaymentId)
        );

        if (!foundPayment) {
          setError("Payment not found.");
          return;
        }

        setPayment(foundPayment);

        const foundOrder = ordersResponse.data.find(
          (order) => order.id === foundPayment.order_id
        );

        if (!foundOrder) {
          setError("Order associated with this payment was not found.");
          return;
        }

        setOrder(foundOrder);
      })
      .catch((error) => {
        console.error(error);
        setError("Failed to load payment information.");
      });
  }, [urlPaymentId]);

  const handleVerify = async (event) => {
    event.preventDefault();

    if (!paymentId || !file) {
      setError("Please select a receipt.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await api.post(
        `/payments/${paymentId}/verify-image`,
        formData
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);

      if (error.response) {
        setError(
          error.response.data.detail ||
          "Payment verification failed."
        );
      } else {
        setError("Could not connect to the backend.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Verify Payment</h1>

      {error && (
        <div>
          <h3>Error</h3>
          <p>{error}</p>
        </div>
      )}

      {payment && order && (
        <div>
          <h2>Order Information</h2>

          <p>
            <strong>Order:</strong> {order.order_number}
          </p>

          <p>
            <strong>Customer:</strong> {order.customer_name}
          </p>

          <p>
            <strong>Expected Amount:</strong>{" "}
            LKR {Number(order.expected_amount).toLocaleString()}
          </p>

          <hr />

          <h2>Payment Information</h2>

          <p>
            <strong>Payment ID:</strong> {payment.id}
          </p>

          <p>
            <strong>Payment Amount:</strong>{" "}
              LKR {Number(payment.amount).toLocaleString()}
            </p>

            <p>
              <strong>Amount Check:</strong>{" "}
              {amountMatches ? (
                <span className="status verified">
                  ✓ MATCHED
                </span>
              ) : (
                <span className="status rejected">
                  ✗ MISMATCH
                </span>
              )}
            </p>

          <p>
            <strong>Payment Method:</strong>{" "}
            {payment.payment_method}
          </p>

          <p>
            <strong>Transaction ID:</strong>{" "}
            {payment.transaction_id}
          </p>

          <p>
            <strong>Payment Status:</strong>{" "}
            {payment.status.toUpperCase()}
          </p>

          <hr />
        </div>
      )}

      <form onSubmit={handleVerify}>
        <div>
          <label>Payment ID</label>
          <br />

          <input
            type="number"
            value={paymentId}
            onChange={(event) => setPaymentId(event.target.value)}
            readOnly={Boolean(urlPaymentId)}
          />
        </div>

        <br />

        <div>
          <label>Payment Receipt</label>
          <br />

          <input
            type="file"
            accept="image/*"
            onChange={(event) =>
              setFile(event.target.files[0])
            }
          />
        </div>

        <br />

        <button type="submit" disabled={loading}>
          {loading ? "Verifying..." : "Verify Payment"}
        </button>
      </form>

      {result && (
        <div>
          <h2>Verification Result</h2>

          <h3>
            {result.status === "VERIFIED"
              ? "✓ Payment Verified"
              : "✗ Payment Rejected"}
          </h3>

          <p>
            <strong>Status:</strong> {result.status}
          </p>

          {result.payment_id && (
            <p>
              <strong>Payment ID:</strong>{" "}
              {result.payment_id}
            </p>
          )}

          {result.transaction_id && (
            <p>
              <strong>Transaction ID:</strong>{" "}
              {result.transaction_id}
            </p>
          )}

          {result.amount !== undefined && (
            <p>
              <strong>Amount:</strong>{" "}
              LKR {result.amount}
            </p>
          )}

          {result.payment_method && (
            <p>
              <strong>Payment Method:</strong>{" "}
              {result.payment_method}
            </p>
          )}

          {result.mismatches &&
            result.mismatches.length > 0 && (
              <div>
                <h4>Problems Found</h4>

                <ul>
                  {result.mismatches.map(
                    (mismatch, index) => (
                      <li key={index}>
                        {mismatch}
                      </li>
                    )
                  )}
                </ul>
              </div>
            )}

          {result.message && (
            <p>
              <strong>Message:</strong>{" "}
              {result.message}
            </p>
          )}
        </div>
      )}
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Dashboard</Link> |{" "}
        <Link to="/orders">Orders</Link> |{" "}
        <Link to="/verify-payment">Verify Payment</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/orders" element={<Orders />} />
        <Route path="/verify-payment" element={<VerifyPayment />} />
        <Route path="/verify-payment/:paymentId" element={<VerifyPayment />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;