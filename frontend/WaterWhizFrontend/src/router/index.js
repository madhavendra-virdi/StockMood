import Vue from 'vue'
import Router from 'vue-router'
import AppLayout from '../layouts/AppLayout'
import Contact from '@/pages/Contact.vue'
Vue.use(Router)

const NotFound = () => import('../pages/404')

const Home = () => import('../pages/Home')

const Insights = () => import('../pages/Insights')
const verify = () => import('../pages/verify')


const Login = () => import('../pages/login')

const Register = () => import('../pages/Register');
const Profile = () => import('../pages/Profile');

const Pricing = () => import('../pages/Pricing');
const aboutCom= () => import('../pages/InsightsCom/aboutCom.vue');




const router = new Router({
  routes: [

    {
      name: 'index',
      path: '/',
      redirect: 'home'
    },
    {
      name: 'verify',
      path: '/verify',
      meta: {
        title: 'verify'
      },
      component: verify
    },
    {
  name: 'layout',
  path: '',
  component: AppLayout,
  children: [
    {
      name: 'home',
      path: '/home',
      meta: { title: 'Home' },
      component: Home
    },
    {
      name: 'insights',
      path: '/insights',
      meta: { title: 'Insights' },
      component: Insights
    },
    {
      name: 'profile',
      path: '/profile',
      meta: { title: 'Profile' },
      component: Profile
    },
    {
      name: 'pricing',
      path: '/pricing',
      meta: { title: 'Pricing' },
      component: Pricing
    },
    {
      name: 'aboutCom',
      path: '/aboutCom',
      meta: { title: 'About Company' },
      component: aboutCom
    },
    {
    name: 'contact',
    path: '/contact',
    meta: { title: 'Contact Us' },
    component: Contact
  }
  ]
}
,
    {
      name: 'register',
      path: '/register',
      meta: { title: 'Register' },
      component: Register
    },
    {
      name: 'login',
      path: '/login',
      meta: {
        title: 'Login'
      },
      component: Login
    },
    {
      path: "/:path(.*)", component: NotFound
    }
  ]
});



export default router
