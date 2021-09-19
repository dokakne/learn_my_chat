var user = { id: -1, email: "", password: "", name: "" };

function auth_guard(callback) {
  axios
    .get("/user", {
      headers: get_auth_header(),
    })
    .then((response) => {
      if (response.data && response.data.email) {
        user = response.data;
        callback();
      } else {
        window.location.href = "/login";
      }
    })
    .catch((error) => {
      window.location.href = "/login";
    });
}

function get_auth_header() {
  return { Authorization: `Bearer ${Cookies.get("email")}` };
}
