<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Orders</h1>
        <hr>
        <div>
            <b-alert dismissible v-model="showMessage" fade variant="success">{{message}}</b-alert>
            <b-alert dismissible v-model="showErrorMessage" fade variant="danger">{{errorMessage}}</b-alert>
        </div>
        <!-- <alert  :message=error_message v-if="showErrorMessage"></alert> -->
        <button type="button"
        class="btn btn-success btn-sm" v-b-modal.book-modal>Create order</button>
        <button type="submit" @click.prevent="logOut()" class="btn btn-primary">LogOut</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Order ID</th>
              <th scope="col">Card ID</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(order, index) in orders" :key="index">
              <td>{{ order.id }}</td>
              <td>{{ order.card_id }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button
                          type="button"
                          class="btn btn-danger btn-sm"
                          @click="onDeleteOrder(order)">
                      Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addBookModal"
            id="book-modal"
            title="Create a new order"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-title-group"
                    label="Card ID:"
                    label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="number"
                        min=1
                        v-model="addOrderForm.card_id"
                        required
                        placeholder="Enter card id">
          </b-form-input>
        </b-form-group>

        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
    props: ['user_id'],
    data() {
        return {
        orders: [],
        endpoint: '',
        
        addOrderForm: {
          card_id: '',
        },
        message: '',
        showMessage: false,
        errorMessage: '',
        showErrorMessage: false,
        // editForm: {
        //   id: '',
        //   title: '',
        //   author: '',
        //   read: [],
        // },
        };
    },
  components: {
    alert: Alert,
  },
  methods: {
      logOut(){
          localStorage.setItem('token', "");
          localStorage.setItem('refresh_token', "");
          
          const path = '/';
          window.location = path
      },

      getOrders() {

        const config = {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      };
      
      const path = 'http://localhost:8080/user/' + this.user_id + '/order';
      axios.get(path, config)
        .then((res) => {
          this.orders = res.data.orders;
          console.log(this.orders);
        })
        .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
        });
    },
    addOrder(payload) {
      const config = {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      };
      
      const path = 'http://localhost:8080/user/' + this.user_id + '/order';
      axios.post(path, payload, config)
        .then((res) => {
            this.message = 'Order added!';
            this.showMessage = true;
            this.getOrders();
        })
        .catch((error) => {
            this.errorMessage = error.response.data.message
            this.showErrorMessage = true;
            console.error(error);
            this.getOrders();
        });
    },
    initForm() {
      this.addOrderForm.card_id = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addBookModal.hide();
      const payload = {
        card_id: this.addOrderForm.card_id,
      };
      this.addOrder(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addBookModal.hide();
      this.initForm();
    },
    removeOrder(orderID) {
      const config = {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      };
      
      const path = 'http://localhost:8080/user/' + this.user_id + '/order/' + orderID;
      axios.delete(path, config)
        .then(() => {
            this.message = 'Order removed!';
            this.showMessage = true;
            this.getOrders(this.user_id);
        })
        .catch((error) => {
            // eslint-disable-next-line
            this.errorMessage = error.response.data.message;
            this.showErrorMessage = true;
            console.error(error.message);
        });
    },
    onDeleteOrder(order) {
      this.removeOrder(order.id);
    },
  },
  created() {
    this.getOrders();
  },
};
</script>
