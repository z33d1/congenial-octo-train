<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">        
        <div style="position:absolute; right:0;">
          <router-link to="/auth" tag="button">Login</router-link>
          <button type="submit" @click.prevent="logOut()" class="btn btn-primary">LogOut</button>
        </div>
        
        <h2>Cards</h2>
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
              <th scope="col">Name</th>
              <th scope="col">Attendance</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(card, index) in pageOfItems" :key="index">
              <td>{{ card.id }}</td>
              <td>{{ card.Name }}</td>
              <td>{{ card.Attendance }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button
                          type="button"
                          class="btn btn-danger btn-sm"
                          @click="onDeleteCard(card)">
                      Delete
                  </button>
                  <br>
                  <button
                          type="button"
                          class="btn btn-primary btn-sm"
                          @click="onUsersForCardClick(card)">
                      Get users
                  </button>
                </div>
              </td>
            </tr>
          </tbody>       
        </table>
        <div class="card-footer pb-0 pt-3">
          <jw-pagination :items="cards" @changePage="onChangePage"></jw-pagination>
        </div>  
    </div>
  </div>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      cards: [],
      pageOfItems: [],
      addBookForm: {
        title: '',
        author: '',
        read: [],
      },
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
    logOut(){
      localStorage.setItem('token', "");
      localStorage.setItem('refresh_token', "");
      localStorage.setItem('role', "");
      
      const path = '/';
      this.$router.push(path)
    },
    onChangePage(pageOfItems) {
            this.pageOfItems = pageOfItems;
    },
    getCards() {
      const path = window.location.protocol + "//" + window.location.hostname + ':' + process.env.VUE_APP_GW_PORT + '/card';
      console.log(path)
      axios.get(path)
        .then((res) => {
          this.cards = res.data.cards;
        })
        .catch((error) => {
          // eslint-disable-next-line
          this.errorMessage = error.response.data.message;
          this.showErrorMessage = true;
          console.error(error);
        });
    },
   
    removeCard(cardID) {
      const path = window.location.protocol + "//" + window.location.hostname + ':' + process.env.VUE_APP_GW_PORT + `/card/${cardID}`;

      if (localStorage.role != 'admin') {
        this.errorMessage = "Access denied.";
        this.showErrorMessage = true;
        console.error(error);
      }
      else {
        axios.delete(path)
        .then(() => {
          this.message = 'Card removed!';
          this.showMessage = true;
          this.getCards();
        })
        .catch((error) => {
          // eslint-disable-next-line
          this.errorMessage = error.response.data.message;
          this.showErrorMessage = true;
          console.error(error);
        });
      }      
    },

    onDeleteCard(card) {
      this.removeCard(card.id);
    },

    onUsersForCardClick(card)
    {
      const path = '/card/' + card.id + '/user';
      this.$router.push(path)
    }
},
  created() {
    this.getCards();
  },
};
</script>
