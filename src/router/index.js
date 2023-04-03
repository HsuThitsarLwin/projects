import { createRouter, createWebHistory } from "vue-router";
import SignIn from "../views/signup/SignIn.vue"
import Reward from "../views/rewards/RewardPage.vue"
import RewardDetails from "../views/rewards/RewardDetails.vue"

const routes = [
    {
        path: '/signin',
        name: "Sign In",
        component: SignIn
    },
    {
        path: '/reward',
        name: "Reward Page",
        component: Reward
    },
    {
        path: '/rewarddetails',
        name: "Reward Details",
        component: RewardDetails
    },
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

export default router