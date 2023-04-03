<script setup>
  console.log(sessionStorage.getItem('cid'));

  if (sessionStorage.getItem('cid') != null) {
    console.log('is authenticated!');
  } else {
    window.location.href = 'http://localhost:5173/signin';
  }
</script>

<script>
import { defineComponent } from 'vue';
import { GoogleMap, Marker } from 'vue3-google-map';
import Nav from '../../components/Nav.vue';

export default defineComponent({
  name: 'App',
  components: {
    Nav
  },
  data() {
    return {
      rewardDetails: [],
      imgs: [
        'https://unsplash.it/1200/768.jpg?image=251',
        'https://unsplash.it/1200/768.jpg?image=252',
        'https://unsplash.it/1200/768.jpg?image=253',
      ], // Img Url , string or Array of string
      visible: false,
      modalVisible: false,
      modalVisible_two: false,
      rid: null,
      startdatetime: '',
      enddatetime: '',
      promopoints: null,
      cid: sessionStorage.getItem('cid')
    };
  },
  computed: {
    getRid() {
      return this.$route.query.rid;
    },
  },
  methods: {
    showModal() {
      this.modalVisible = true;
    },
    confirmRedemption() {
      // handle redeem confirmation here
      // ...

      // set the id property to the ID collected from the user input
      this.rid = this.rewardDetails.rid

      // make HTTP request to execute the Python script
      axios.post('http://127.0.0.1:5800/redeemRewards', { 
        params: {
          rid: this.rid, 
          cid: this.cid 
        }
      })
      .then(response => {
        alert(response.data['data'])
        window.location.reload() 
      })
      .catch(error => {
        alert(response.data['data'])
        window.location.reload() 
      });
    },
    confirmSpecialOffer() {
      if(sessionStorage.getItem('cid')==9999){
        var apiValue = 'NJ67JJJQaWebzWzH1JwP57vHcv5INGXQ'
      }
      // set the id property to the ID collected from the user input
      this.rid = this.rewardDetails.rid

      // make HTTP request to execute the Python script
      axios.put('http://localhost:8000/api/v1/specialOffer', { 
        params:{
          rid: this.rid,
          startdatetime: this.startdatetime,
          enddatetime: this.enddatetime,
          promopoints: this.promopoints,
          }
        },
        {
          headers:{
            apikey: apiValue
        },
      })
      .then(response => {
        alert(response.data['data'])
        window.location.reload()
      })
      .catch(error => {
        alert(response.data['message'])
        window.location.reload() 
      });
    },
    show() {
      this.visible = true;
    },
    getRewardDetails() {
      const rid = this.getRid;
      axios
        .get('http://127.0.0.1:5000/reward/'+ rid)
        .then((response) => {
          this.rewardDetails = response.data.data;
        })
        .catch((error) => alert(error));
    },
  },
  mounted: function () {
    this.getRewardDetails();
  },
});
</script>

<template>
  <Nav style="z-index: 3" />

  <!-- Start of Container-->
  <div class="container">
    <!-- For The Three Images at the Top-->
    <div class="row gallery">
      <div
        v-for="(img, idx) in imgs"
        :key="idx"
        :id="'image' + idx"
        class="col pic"
        @click="() => show(idx)"
      >
        <img :src="img.src ? img.src : img" style="width: 100%" />
      </div>
    </div> <!-- End of For The Three Images at the Top-->

    <!-- Separator Div -->
    <div class="row mt-3"> 
      <!-- Start of Left Side -->
      <div class="col-xl-8 col-md-12 col-s-12 order-3 order-md-2">
        <!-- Reward Name and Description -->
        <div class="row"> 
          <div class="card">
            <div class="card-body">
              <p class="h2 fw-bold">{{this.rewardDetails.rewardName}}</p>
              <br>
              <p> {{ this.rewardDetails.reward_description }} </p>
            </div>
          </div>
        </div> <!-- End of Reward Name and Description -->

        <!-- Map  -->
        <div class="row mt-3">
          <div class="card">
            <div class="card-body">
              <p class="h2 fw-bold">Location</p>
              <GoogleMap
                api-key="AIzaSyBkQ_V1LdDab3pFbzuJeg5Jjh5ofQYfx9k"
                class="map"
                :center="{ lat: this.rewardDetails.latitude, lng: this.rewardDetails.longitude }"
                :zoom="15"
              >
              <Marker :options="{ position: { lat: this.rewardDetails.latitude, lng: this.rewardDetails.longitude } }" />
              </GoogleMap>
            </div>
          </div>
        </div> <!-- End of Map -->

      </div> <!-- End of Left Side -->

      <!-- Start of Right Side  -->
      <div id="details-page" class="col-xl-4 col-xs-12 order-2 order-md-3">
        <div class="card"> <!-- Outer Box -->
          <div class="card-body"> <!-- Inner Box -->

            <!-- Start of Top Half -->
            <div class="row pt-3 ps-3">
              <ul>
                <li class="list-group-item mt-2">
                  <i class="bi bi-trophy"></i>
                  &nbsp; Tier: {{ this.rewardDetails.rewardTier }}
                </li>
                <li class="list-group-item mt-2">
                  <i class="bi bi-archive"></i>
                  &nbsp; Quantity: {{ this.rewardDetails.quantity }}
                </li>
                <li v-if="rewardDetails.promo_points != null" class="list-group-item mt-2">
                  <i class="bi bi-award"></i>                    
                  &nbsp; Points: <span style="text-decoration: line-through;">{{ rewardDetails.points }} </span> {{ rewardDetails.promo_points }}
                </li>
                <li v-else class="list-group-item mt-2">
                  <i class="bi bi-award"></i>                    
                  &nbsp; Points: {{ this.rewardDetails.points }}
                </li>
                <li class="list-group-item mt-2">
                  <i class="bi bi-compass"></i>
                  &nbsp; Region: {{ this.rewardDetails.region }}
                </li>
              </ul>
            </div> <!-- End of Top Half -->

            <hr />

            <!-- Start of Bottom Half -->
            <div class="row pt-3 ps-2">
              
              <!-- Create Special Offer-->
              <button id="create-offer-btn" class="btn btn-primary btn-apply btn-lg" type="button" v-if="this.cid==9999" data-bs-toggle="modal" data-bs-target="#specialBox" @click="showModal()">
                Create Special Offer
              </button>

              <!-- Redemption Button -->
              <button id="redeem-now-btn" class="btn btn-primary btn-apply btn-lg" type="button" v-else data-bs-toggle="modal" data-bs-target="#redeemBox" @click="showModal()">
                Redeem Now
              </button>

              <!-- IF Special Offer Dialog Box -->
              <div class="modal fade" id="specialBox" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="specialLabel" aria-hidden="true">
                <!-- Start of Dialog Box Inner 1 -->
                <div class="modal-dialog">
                  <!-- Start of Dialog Box Inner 2 -->
                  <div class="modal-content">
                    <!-- Start of Dialog Box Header -->
                    <div class="modal-header">
                      <h1 class="modal-title fs-5" id="specialLabel">Create Special Offer</h1>
                      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div> <!-- End of Dialog Box Header-->
                    <!-- Start of Dialog Box Body -->
                    <form>
                      <div class="modal-body">
                        Reward Name: {{this.rewardDetails.rewardName}} 
                        <br>
                        Current Points: {{ this.rewardDetails.points}}
                        <hr>

                        <label for="startdatetime">Start Date and Time:</label>
                        <input type="datetime-local" id="startdatetime" v-model="startdatetime" required>

                        <label for="enddatetime">End Date and Time:</label>
                        <input type="datetime-local" id="enddatetime" v-model="enddatetime" required>

                        <label for="promopoints">Promotional Points:</label>
                        <input type="number" id="promopoints" min="1" max="99999" 
                        v-model="promopoints" required><br><br> <!-- End of Dialog Box Body -->
                        <!-- Start of Dialog Box Footer -->
                        <div class="modal-footer">
                          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" >Close</button>
                          <button type="button" class="btn btn-primary" @click="confirmSpecialOffer()">Confirm</button>
                        </div> <!-- End of Dialog Box Footer -->
                      </div>
                    </form>
                  </div> <!-- End of Dialog Box Inner 2 -->
                </div> <!-- End of Dialog Box Inner 1 -->
              </div> <!-- End of Dialog Box -->

              <!-- ELSE Confirmation Dialog Box -->
              <div class="modal fade" id="redeemBox" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="redeemLabel" aria-hidden="true">
                <!-- Start of Dialog Box Inner 1 -->
                <div class="modal-dialog">
                  <!-- Start of Dialog Box Inner 2 -->
                  <div class="modal-content">
                    <!-- Start of Dialog Box Header -->
                    <div class="modal-header">
                      <h1 class="modal-title fs-5" id="redeemLabel">Confirmation Dialog</h1>
                      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"
                        @click="hideModal()"></button>
                    </div> <!-- End of Dialog Box Header-->
                    <!-- Start of Dialog Box Body -->
                    <div class="modal-body">
                      <p>Are you sure you want to redeem this?</p>
                    </div> <!-- End of Dialog Box Body -->
                    <!-- Start of Dialog Box Footer -->
                    <div class="modal-footer">
                      <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" >Cancel </button>
                      <button id="confirm-redeem-btn" type="button" class="btn btn-primary" @click="confirmRedemption()">Confirm
                        Redemption</button>
                    </div> <!-- End of Dialog Box Footer -->
                  </div> <!-- End of Dialog Box Inner 2 -->
                </div> <!-- End of Dialog Box Inner 1 -->
              </div> <!-- End of Dialog Box -->

            </div> <!-- End of Bottom Half -->
          </div> <!-- End of Inner Box -->
        </div> <!-- End of Outer Box -->
      </div> <!-- End of Right Side -->
    </div> <!-- End of Separator Div -->
  </div> <!-- End of Container -->
</template>

<style scoped>

h1, h2, h3, h4, h5, h6, p {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.list-group,
.list-group-item {
  border-style: none;
}

.btn-apply {
  background-color: #4a60e8;
}
</style>

<style>
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  position: static;
  font-weight: normal;
}

.map {
  height: 500px;
}
</style>
