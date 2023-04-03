<script setup>
  console.log(sessionStorage.getItem('cid'));

  if (sessionStorage.getItem('cid') != null) {
    console.log('is authenticated!');
  } else {
    window.location.href = 'http://localhost:5173/signin';
  }
</script>

<script>
import Nav from '../../components/Nav.vue';
import * as Main from '../../main';

export default {
  name: 'App',
  components: {
    Nav,
  },
  data() {
    return {
      reward_details: [],
      search: '',
      category: '',
      categories: ['Technology', 'Food', 'Entertainment'],
      categories_details: {
        Technology: 'badge text-bg-primary',
        Food: 'badge text-bg-warning',
        Entertainment: 'badge text-bg-success',
      },

      regions: ['North', 'South', 'East', 'West', 'Central'],
      showSpecialOfferOnly: false,

      reward_img: [
        {
          Technology: 'src/assets/rewardsImg/technology.jpg',
          Food: 'src/assets/rewardsImg/food.jpg',
          Entertainment: 'src/assets/rewardsImg/entertainment.jpg',
        },
      ],
    };
  },
  computed: {
    filteredList() {
      var categories = [];
      var regions = [];

      for (const category of this.categories) {
        categories.push(category.toLowerCase());
      }
      for (const region of this.regions) {
        regions.push(region.toLowerCase());
      }

      var dateList = this.reward_details.filter((reward) => {
        return reward.rewardName;
      });

      var searchedList = dateList.filter((reward) => {
        return (
          reward.rewardName.toLowerCase().includes(this.search.toLowerCase())
        );
      });

      return Array.prototype.filter.call(searchedList, (reward) => {
        return (
          categories.includes(reward.category.toLowerCase()) &&
          regions.includes(reward.region.toLowerCase()) &&
          (this.showSpecialOfferOnly ? reward.is_specialOffer == '1' : true)
        );
      });
    },
  },

  methods: {
    get_details() {
      axios
        .get('http://127.0.0.1:5000/reward')
        .then((response) => {
          this.reward_details = response.data.data.rewards;
          
        })
        .catch((error) => alert(error));
    },
    getImgUrl(path) {
      var str = 'src/assets/' + path;
      return str;
    },
    checkCat(cardCat) {
      for (const category of this.categories) {
        if (category != cardCat) {
          // console.log(category + ' ' + cardCat + ' there is no match');
          continue;
        } else {
          // console.log(category + ' ' + cardCat + ' there is a match');
          return true;
        }
      }
    },
  },
  created: function () {
    this.get_details();
    this.getImgUrl();
  },
};
</script>

<template>
  <Nav style="z-index: 3" />

  <div class="container pb-5">
    <div class="row">
      <div class="col">
        <div class="searchFilter m-3 mx-auto">
          <div class="hstack gap-2">
            <input type="search" class="form-control" id="search" placeholder="What Are You Looking For?"
              v-model.trim="search" />

            <button type="button" class="btn btn-outline-secondary btn-sm dropdown-toggle ms-auto"
              data-bs-toggle="dropdown" data-bs-auto-close="outside" aria-expanded="false">
              <i class="bi bi-funnel-fill"></i>
              <span id="filterText">Filter</span>
            </button>
            
            <!-- Filter Section-->
            <ul class="dropdown-menu">
              <li>
                <h6 class="dropdown-header">Category</h6>
              </li>
              <li class="dropdown-item">
                <input type="checkbox" value="Technology" id="technology" v-model="categories" /><label class="w-100"
                  for="technology">&nbsp;Technology</label>
              </li>
              <li class="dropdown-item">
                <input type="checkbox" value="Food" id="food" v-model="categories" /><label class="w-100"
                  for="food">&nbsp;Food</label>
              </li>
              <li class="dropdown-item">
                <input type="checkbox" value="Entertainment" id="entertainment" v-model="categories" /><label class="w-100"
                  for="entertainment">&nbsp;Entertainment</label>
              </li>
              
              <li>
                <hr class="dropdown-divider" />
              </li>

              <li>
                <h6 class="dropdown-header">Region</h6>
              </li>
              <li class="dropdown-item">
                <input type="checkbox" value="North" id="north" v-model="regions" /><label class="w-100"
                  for="north">&nbsp;North</label>
              </li>
              <li class="dropdown-item">
                <input type="checkbox" value="South" id="south" v-model="regions" /><label class="w-100"
                  for="south">&nbsp;South</label>
              </li>
              <li class="dropdown-item">
                <input type="checkbox" value="East" id="east" v-model="regions" /><label class="w-100"
                  for="east">&nbsp;East</label>
              </li>
              <li class="dropdown-item">
                <input type="checkbox" value="West" id="west" v-model="regions" /><label class="w-100"
                  for="west">&nbsp;West</label>
              </li>
              <li class="dropdown-item">
                <input type="checkbox" value="Central" id="central" v-model="regions" /><label class="w-100"
                  for="central">&nbsp;Central</label>
              </li>

              <li>
                <hr class="dropdown-divider" />
              </li>
              <li class="dropdown-item">
                <input type="checkbox" id="show-special-offers" v-model="showSpecialOfferOnly" /><label class="w-100"
                  for="show-special-offers">&nbsp;Special Offer</label>
              </li>


            
            </ul>
          </div>
        </div>
      </div>
    </div>
    <!--cards -->

    <div class="col col-sm-12">
      <h3 class="row fw-bold text-dark ms-4">Recommended For You</h3>
      <br />
      <div class="row mx-auto container">
        <div v-for="reward in filteredList" :key="reward.rid" class="mt-4 col-12 col-sm-6 col-md-4">
          <div class="card glass">
            <!-- Images -->
            <a class="nav-link" :href="'/rewarddetails?rid=' + reward.rid">
              <div class="card-header card-image">
                <img id="card-img" class="mb-2 rounded" v-if="checkCat(reward.category)"
                :src="reward_img[0][reward.category]" />
              </div>
            </a>

            <div class="card-body mb-1">
              <!-- Reward Name -->
              <h5 class="h3">{{ reward.rewardName }}</h5>
              <span v-if='reward.promo_points != null' class="badge bg-danger">Special Offer</span>
              <br />

              <!-- Quantity-->
              <i class="bi bi-bag"></i>
              <h6 class="fw-normal">&nbsp;&nbsp;{{ reward.quantity }} Remaining</h6>
              <br />

              <!-- Points -->
              <i class="bi bi-currency-exchange"></i>
              <h6 v-if='reward.promo_points != null' class="fw-normal" >
                &nbsp;
                <span style="text-decoration: line-through;">{{ reward.points }} </span>
                {{ reward.promo_points }} Points
              </h6>
              <h6 v-else class="fw-normal">&nbsp;&nbsp;{{ reward.points }} Points</h6>
              <br />

              <!-- Location -->
              <i class="bi bi-geo-alt-fill"></i>
              <h6 class="fw-normal">&nbsp;{{ reward.region }}</h6>

              <!-- Badge -->
              <div class="d-flex justify-content-end">
                <h5>
                  <span :class="this.categories_details[reward.category]">
                    {{ reward.category }}</span>
                </h5>
              </div>


            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<!-- Styling CSS -->
<style scoped>
#bg_img {
  position: fixed;
  min-height: 100px;
  min-width: 1024px;
  width: 100%;
  height: auto;
  top: 0;
  bottom: 0;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.card {
  --padding: 0.8rem;
  border-radius: 0.25rem;
  overflow: hidden;
}

.card-header {
  font-size: 1.5rem;
  padding: var(--padding);
  padding-bottom: 0;
  margin-bottom: 0.5rem;
}

.card-header.card-image {
  padding: 4;
  overflow: hidden;
}

.card-header.card-image>img {
  display: block;
  width: 100%;
  max-height: 200px;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  object-position: center;
  transition: 200ms transform ease-in-out;
}

.card:hover>.card-header.card-image>img {
  transform: scale(1.025);
}

.card-body {
  font-size: 0.9rem;
  padding: 0 1rem;
  background: linear-gradient(0deg,
      rgba(255, 255, 255, 0.5),
      rgba(255, 255, 255, 0.5)),
    linear-gradient(114.55deg, #dfe3fc 0%, #e2dffe 98.46%);
}

h6,
svg {
  display: inline;
}

h3 {
  position: absolute;
}

.searchFilter {
  width: 90%;
}

#filterText {
  display: none;
}

@media (min-width: 391px) {
  .searchFilter {
    width: 50%;
  }

  #filterText {
    display: inline-block;
  }
}

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  position: relative;
  font-weight: normal;
}

.btn:hover {
  background-color: gray !important;
}

.btn {
  background-color: transparent !important;
  border: 1px solid gray;
}
</style>
