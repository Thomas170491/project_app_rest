const token = localStorage.getItem("access_token");

export const isLoggedIn = () => {
    console.log('Logged in:', token !== null)
    
    return token !== null
  };