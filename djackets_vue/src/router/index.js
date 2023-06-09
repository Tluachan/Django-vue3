import { createRouter, createWebHistory } from 'vue-router'

import store from '../store'

import HomeView from '../views/HomeView.vue'
import Product from '../views/Product.vue'
import Category from '../views/Category.vue'
import Search from '../views/Search.vue'
import SignUp from '../views/SignUp.vue'
import LogIn from '../views/LogIn.vue'
import MyAccount from '../views/MyAccount.vue'
import ShowCategory from '../views/ShowCategory.vue'
import Review from '../views/AddReview.vue'
import ShopOwner from '../views/ShopOwner.vue'
import AboutView from '../views/AboutView.vue'
import ContactView from '../views/ContactView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'AboutView',
    component: AboutView

  },
  {
    path: '/contact',
    name: 'ContactView',
    component: ContactView

  },

  {
    path: '/search',
    name: 'Search',
    component: Search
  },

  {
    path: '/sign-up',
    name: 'SignUp',
    component: SignUp
  },

  {
    path: '/log-in',
    name: 'LogIn',
    component: LogIn
  },

  {
    path: '/my-account',
    name: 'MyAccount',
    component: MyAccount,
    meta: {
      requireLogin: true
    }
  },

  {
    path: '/:category_slug/:product_slug',
    name: 'Product',
    component: Product
  },

  {
    path: '/:category_slug',
    name: 'Category',
    component: Category
  },
  {
    path: '/category',
    name: 'ShowCategory',
    component: ShowCategory
  },

  {
    path: '/:category_slug/:product_slug/addreviews',
    name: 'Review',
    component: Review,
    props: true,
    meta: {
      requireLogin: true
    }
  },

  {
    path: '/user/shop-owner-view',
    name: 'ShopOwner',
    component: ShopOwner,
    meta: {
      requireLogin: true
    }
  }
  

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

//Check the log in status before associating with my account page (check token first)
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next({ name: 'LogIn', query: { to: to.path } });
  } else {
    next()
  }
})

export default router
