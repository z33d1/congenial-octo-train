<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">        
        <h2>Card Users</h2>
        <hr>
        <div>
            <b-alert dismissible v-model="showMessage" fade variant="success">{{message}}</b-alert>
            <b-alert dismissible v-model="showErrorMessage" fade variant="danger">{{errorMessage}}</b-alert>
        </div>
        <!-- <button type="button"
        class="btn btn-success btn-sm" v-b-modal.book-modal>Add Book</button> -->
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Id</th>
              <th scope="col">UserName</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in users" :key="index">
              <td>{{ user.user_info.id }}</td>
              <td>{{ user.user_info.username }}</td>
            </tr>
          </tbody>       
        </table>

    </div>
  </div>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
    props: ['card_id'],
    data() {
        return {
        users: [],

        message: '',
        showMessage: false,
        errorMessage: '',
        showErrorMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getUsers() {
      const path = window.location.hostname + ':' + process.env.VUE_APP_GW_PORT + '/card/'+ this.card_id + '/user';
      axios.get(path)
        .then((res) => {
          this.users = res.data.users_for_this_card;
          console.log(res.data.users_for_this_card);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
   
    removeCard(cardID) {
      const path = window.location.hostname + ':' + process.env.VUE_APP_GW_PORT + `/card/${cardID}`;
      axios.delete(path)
        .then(() => {
          this.getCards();
          this.message = 'Card removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          this.errorMessage = error.response.data.message
          this.showErrorMessage = true;
          console.error(error);
          this.getCards();
        });
    },

    onDeleteCard(card) {
      this.removeCard(card.id);
    },

},
  created() {
    this.getUsers();
  },
};
</script>
