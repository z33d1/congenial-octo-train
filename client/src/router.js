import Vue from 'vue';
import Router from 'vue-router';
import Cards from './components/Cards.vue';
import Users from './components/Users.vue';
import Orders from './components/Orders.vue';
import CardUsers from './components/CardUsers.vue';
import Auth from './components/Auth.vue';
import HelloWorld from './components/HelloWorld.vue';


Vue.use(Router);

export default new Router({
  mode: 'history',
  // base: process.env.BASE_URL,
  routes: [
    {
      path: '/auth',
      name: 'Auth',
      component: Auth,
    },
    {
      path: '/',
      name: 'Cards',
      component: Cards,
    },
    {
      path: '/user',
      name: 'User',
      component: Users,
    },
    {
      path: '/user/:user_id/order',
      name: 'Orders',
      component: Orders,
      props: true,
    },
    {
      path: '/card/:card_id/user',
      name: 'CardUsers',
      component: CardUsers,
      props: true,
    },
    {
      path: '/hw',
      component: HelloWorld
    }
  ],
});
