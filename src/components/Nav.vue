<script>
export default {
  data() {
    return {
      balance_points: '',
      name: '',
      cid: sessionStorage.getItem('cid'),
    };
  },
  methods: {
    logout() {
      sessionStorage.clear();
      window.location.href = 'http://localhost:5173/signin';
    },
    get_balance() {
      axios
        .get('http://127.0.0.1:5200/customer/' + this.cid)
        .then((response) => {
          this.balance_points = response.data.data.balancePoints;
          this.name = response.data.data.name;
        })
        .catch((error) => alert(error));
    },
    generateCharts() {
      axios
        // .get('http://127.0.0.1:4010/graphql_aggregation')
        .get('http://localhost:8000/api/v1/graphql_aggregation')
        .then((response) => {
          window.open(
            'http://127.0.0.1:4020/charts',
            '_blank' // Open new Window
          );
        })
        .catch((error) => alert(error));
    },
  },
  created: function () {
    this.get_balance();
  },
};
</script>

<template>
  <nav class="rounded-bottom navbar navbar-expand-lg navbar-container">
    <div class="mx-5 container-fluid p-0">
      <router-link
        class="fw-bold nav-link navbar-brand"
        style="color: #7a542e"
        to="/reward"
        >RedeemNow</router-link
      >
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
          <!-- <li class="nav-item">
                      <router-link class="nav-link" to="/">Explore</router-link>
            </li> -->

          <li class="nav-item">
            Welcome, {{ name }} ({{ balance_points }} Points)
          </li>

          <div class="nav-link p-0" data-bs-toggle="dropdown">
            <li class="nav-item">
              <button id="imgButton" class="btn btn-default">
                <img src="../assets/xavier.JPG" />
              </button>

              <div class="dropdown-menu dropdown-menu-end">
                <li v-if="this.cid == 9999" @click="generateCharts">
                  <a class="dropdown-item">Dashboard</a>
                </li>
                <li><a class="dropdown-item">Settings</a></li>
                <div class="dropdown-divider"></div>
                <li @click="logout">
                  <a class="dropdown-item"> Log Out</a>
                </li>
              </div>
            </li>
          </div>
        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar-nav {
  display: flex;
  align-items: center;
  justify-content: center;
}

#imgButton {
  font-size: 24px;
  border: none;
  cursor: pointer;
  outline: none;
  margin: auto;
  display: block;
  background-color: transparent !important;
}

#imgButton:hover {
  background-color: transparent !important;
}

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  position: relative;
  font-weight: normal;
}

img {
  width: 35px;
  height: 35px;
  object-fit: cover;
  border-radius: 50%;
}

.navbar-container {
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.3),
    rgba(255, 255, 255, 0.1)
  );
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 2px 22px 0 rgba(0, 0, 0, 0.2);
}
</style>
