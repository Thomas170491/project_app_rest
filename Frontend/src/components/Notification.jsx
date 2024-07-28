import React, { useEffect, useState } from "react";

const Notification = () => {
  const token = localStorage.getItem("access_token");
  const user = JSON.parse(localStorage.getItem("user"));

  const [notiSender, setNotiSender] = useState([]);
  const [notiReceiver, setNotiReceiver] = useState([]);

  const markNoti = async (noti_id) => {
    const response = await fetch("http://localhost:8000/mark-notification/", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ noti_id }),
    });
    const responseBody = await response.json();
    if (responseBody.status === "success") {
      console.log(responseBody);
    } else {
      console.error("Mark notification is failed", responseBody.message);
    }
  };
  const acceptOrder = async (order_id, is_accepted) => {
    const response = await fetch("http://localhost:8000/accept-order/", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ order_id, is_accepted }),
    });
    const responseBody = await response.json();
    if (responseBody.status === "success") {
      console.log(responseBody);
    } else {
      console.error("Cant book the Ride", responseBody.message);
    }
  };

  const getNotifications = async () => {
    const response = await fetch("http://localhost:8000/notification/", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    const responseBody = await response.json();
    if (responseBody.status === "success") {
      setNotiSender(responseBody.data.noti_as_sender);
      setNotiReceiver(responseBody.data.noti_as_receiver);
      console.log(responseBody);
    } else {
      console.error("Cant book the Ride", responseBody.message);
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      getNotifications();
    }, 1000);
    return () => clearInterval(interval);
  }, []);
  return (
    <div>
      <h1>Notifications</h1>
      <table>
        <thead>
          {notiSender.map((noti, index) => (
            <tr key={index}>
              <td>
                {noti.message_sender}
                <div>
                  <button onClick={() => markNoti(noti.id)}>Mark</button>
                </div>
              </td>
            </tr>
          ))}
          {notiReceiver.map((noti, index) => (
            <tr key={index}>
              <td>
                {noti.message_receiver}
                {noti.receiver.role == "driver" ? (
                  <div>
                    <button onClick={() => acceptOrder(noti.order, true)}>
                      Accept
                    </button>
                    <button onClick={() => acceptOrder(noti.order, false)}>
                      Decline
                    </button>
                    <div>
                      <button onClick={() => markNoti(noti.id)}>Mark</button>
                    </div>
                  </div>
                ) : (
                  <div>
                    <button onClick={() => markNoti(noti.id)}>Mark</button>
                  </div>
                )}
              </td>
            </tr>
          ))}
        </thead>
      </table>
    </div>
  );
};

export default Notification;
