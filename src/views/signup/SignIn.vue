<script>
export default {
  name: 'App',
  data() {
    return {
      message: 'Hello, please wait',
      cid: 0
    };
  },
  methods: {
    login() {
      sessionStorage.setItem('cid', this.cid);
      window.location.href = 'http://localhost:5173/reward';
    },
  },
};
</script>

<template>
  <div class="body">
    <section class="vh-100">
      <div class="container py-5 h-100">
        <div class="row d-flex justify-content-center align-items-center h-100">
          <div class="col col-xl-8">
            <div class="card-login">
              <div class="row d-flex align-items-center justify-content-center g-0">
                <div class="col-md-6 col-lg-5 d-none d-md-block items-align-center">
                  <img src="../../assets/login.png" alt="login form" class="" />
                </div>
                <div class="col-md-6 col-lg-7 d-flex align-items-center">
                  <div class="card-body p-4 p-lg-5 text-black">
                    <form>
                      <div class="d-flex align-items-center mb-3 pb-1">
                        <span class="h3 fw-bold mb-0 text-center">Login to Your Account</span>
                      </div>
                      <div class="form-outline mb-4 content-justify-center">
                        <font-awesome-icon icon="fa-solid fa-envelope fa-lg" class="icon icon-pw" />
                        <input type="number" v-model="this.cid" class="form-control form-control-lg" id="cid" placeholder="CID" />
                      </div>

                      <div class="form-outline mb-4 content-justify-center">
                        <font-awesome-icon icon="fa-solid fa-lock fa-lg" class="icon icon-pw" />
                        <input type="password" class="form-control form-control-lg pw-input" id="passwordInput"
                          placeholder="Password" />
                      </div>
                      <div class="d-grid gap-2 text-center">
                        <button type="button" class="btn btn-dark btn-signup btn-outline-light fs-4" @click="login">
                          Sign In
                        </button>
                        <!-- <p class="fs-5">Forget Password?</p> -->
                      </div>

                    </form>

                    <!-- <div class="text-center">
                      <p class="fs-6">Or</p>
                      <div class="g-signin2" data-width="300" data-height="200" data-longtitle="true">
                        <GoogleLogin :callback="callback" />
                      </div>
                      <p class="text-center fs-6" style="color: #393f81">
                        Don't have an account?
                        <router-link to="/signup">Register here </router-link>
                      </p>
                    </div> -->
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.body {
  background-image: url('../../../src/assets/bg_plain.png');
}

img {
  display: flex;
  align-items: center;
  margin: auto;
  width: 100%;
  justify-content: center;
}

.card-login {
  background: linear-gradient(135deg,
      rgba(255, 255, 255, 0.3),
      rgba(255, 255, 255, 0.1));
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}

input {
  padding: 5px 10px 5px 50px;
  display: block;
  width: 100%;
}

.icon {
  position: absolute;
  left: 15px;
  top: 10px;
  font-size: 25px;
  height: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
}

.btn-signup {
  background-color: #3b4f7d;
  border-radius: 10px;
  padding: 10px 0;
}

.btn:hover {
  color: white;
  background-color: #4e5ff4;
  box-shadow: -2px -1px 2px rgba(0, 0, 0, 0.25);
}

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  position: relative;
  font-weight: normal;
}
</style>
