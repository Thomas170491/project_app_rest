import React, { useEffect, useState } from "react";
import { Form } from "react-bootstrap";
const baseUrl = import.meta.env.VITE_REACT_APP_BASE_URL;

const Pay = ({ rideId }) => {
  const [cardnum, setCardnum] = useState("");
  const [cvv, setCvv] = useState("");
  const [exdate, setExdate] = useState("");
  const token = localStorage.getItem("access_token");
  const user = JSON.parse(localStorage.getItem("user"));

  const [price, setPrice] = useState([]);

  const [paymentDetails, setPaymentDetails] = useState(null);

  const payPrice = async (order_id, pay_id) => {
    let card_num = document.querySelector("#card_num").value;
    let expire_data = document.querySelector("#expire_data").value;
    let cvv2 = document.querySelector("#cvv2").value;
    if (card_num.length !== 16) {
      console.log("Card Number is not valid");
    }
    if (cvv2.length !== 3) {
      console.log("CVV2 is not valid");
    }
    const response = await fetch(`${baseUrl}/payment/`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ order_id, pay_id }),
    });
    const responseBody = await response.json();
    if (responseBody.status === "success") {
      console.log(responseBody);
    } else {
      console.error("Failed to do Payments", responseBody.message);
    }
  };
  const handlePay = async () => {
    const response = await fetch(`${baseUrl}/payment/`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    const responseBody = await response.json();
    if (responseBody.status === "success") {
      console.log(responseBody);
      setPrice(responseBody.data);
    } else {
      console.error("Failed to get Payments", responseBody.message);
    }
  };

  useEffect(() => {
    handlePay();
  }, []);

  return (
    <>
      <div>
        <h1>Pay for Ride</h1>
        <div>
          <Form>
            <Form.Group controlId="formUsername">
              <Form.Label>Enter Card Number</Form.Label>
              <Form.Control
                type="text"
                value={cardnum}
                onChange={(e) => setCardnum(e.target.value)}
                placeholder="Enter Card Number"
                id="card_num"
              />
            </Form.Group>
            <Form.Group className="mt-3">
              <Form.Label>Enter Expire Date</Form.Label>
              <Form.Control
                type="date"
                value={exdate}
                onChange={(e) => setExdate(e.target.value)}
                placeholder="Enter Expire Date"
                id="expire_data"
              />
            </Form.Group>
            <Form.Group className="mt-3">
              <Form.Label>Enter CVV2</Form.Label>
              <Form.Control
                type="text"
                value={cvv}
                onChange={(e) => setCvv(e.target.value)}
                placeholder="Enter CVV2"
                id="cvv2"
              />
            </Form.Group>
          </Form>
        </div>
        <table>
          <tbody>
            {price.map((item, index) => (
              <tr key={index}>
                <td>
                  <p>
                    Your Order <strong>#{item.order}</strong> to{" "}
                    <strong>{item.driver.email}</strong> has
                    <strong> Price: {item.total_price}</strong>
                  </p>
                  <button onClick={() => payPrice(item.order, item.id)}>
                    Pay
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
};

export default Pay;
