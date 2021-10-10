import Vue from 'vue';
import Router from 'vue-router';
import Cards from './components/Cards.vue';
import Users from './components/Users.vue';
import Orders from './components/Orders.vue';
import CardUsers from './components/CardUsers.vue';
import Auth from './components/Auth.vue';


Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
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
      path: '/users',
      name: 'Users',
      component: Users,
    },
    {
      path: '/users/:user_id/orders',
      name: 'Orders',
      component: Orders,
      props: true,
    },
    {
      path: '/cards/:card_id/users',
      name: 'CardUsers',
      component: CardUsers,
      props: true,
    },
  ],
});
