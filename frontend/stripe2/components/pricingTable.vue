<template>
  <v-container fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="12">
        <v-card>
          <v-img
            src="https://images.pexels.com/photos/10443572/pexels-photo-10443572.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
            gradient="to top, rgba(0,0,0,0.6), rgba(0,0,0,0.1)" class="white--text align-end" max-height="300px">
            <v-card-title>
              Wombat Subscriptions
            </v-card-title></v-img>
            <v-card-text>

              <script async src="https://js.stripe.com/v3/pricing-table.js"></script>
              <stripe-pricing-table pricing-table-id="prctbl_1MHwPOIlCeH6bP8R4r9w5eGf"
              publishable-key="pk_test_51JticYIlCeH6bP8REulC9GlUO09hWuGsCljwJ3VNWhqqLmTTW0CedWXOoABWyXkplmqMtwfA4SiXkdeqCMvesIii00BCpJb9Vb">
              </stripe-pricing-table>
            </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="12" md="10" lg="8">
        <v-card>
          <v-img
            src="https://images.pexels.com/photos/34225/spider-web-with-water-beads-network-dewdrop.jpg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
            gradient="to top, rgba(0,0,0,0.6), rgba(0,0,0,0.1)" class="white--text align-end" max-height="300px">
            <v-card-title>
              Web Development
            </v-card-title>
          </v-img>
          <v-card-text>
            <stripe-pricing-table pricing-table-id="prctbl_1LO6MbIlCeH6bP8RYDkbYlNH"
              publishable-key="pk_test_51JticYIlCeH6bP8REulC9GlUO09hWuGsCljwJ3VNWhqqLmTTW0CedWXOoABWyXkplmqMtwfA4SiXkdeqCMvesIii00BCpJb9Vb">
            </stripe-pricing-table>

          </v-card-text>
        </v-card>


      </v-col>
    </v-row>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="12" md="10" lg="8">
        <v-card>
          <v-img
            src="https://images.pexels.com/photos/1235706/pexels-photo-1235706.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
            gradient="" max-height="300px" class="white--text align-end">
            <v-card-title>
              I like coffee
            </v-card-title>
          </v-img>
          <v-card-text>

            <stripe-pricing-table pricing-table-id="prctbl_1LO7EdIlCeH6bP8Rw2ihU7ju"
              publishable-key="pk_test_51JticYIlCeH6bP8REulC9GlUO09hWuGsCljwJ3VNWhqqLmTTW0CedWXOoABWyXkplmqMtwfA4SiXkdeqCMvesIii00BCpJb9Vb">
            </stripe-pricing-table>
          </v-card-text>
        </v-card>

      </v-col>
    </v-row>
  </v-container>
</template>


</stripe-pricing-table>
