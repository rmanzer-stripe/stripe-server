<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="12" md="9">
        <v-card>
          <v-img
           :src="config.cardImage"
           gradient="to top, rgba(0,0,0,0.7), rgba(0,0,0,0.2)"
           height="200"
           class="align-end white--text"
           >
            <v-card-title>{{ config.cardTitle }}</v-card-title>
          </v-img>
          <v-card-text>
            <component :is="config.component" :reader="reader"></component>
          </v-card-text>
          <v-card-actions></v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="12" sm="12" md="3">
        <v-card>
          <v-img
            src="https://images.pexels.com/photos/35763/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
            gradient="to top, rgba(0,0,0,0.7), rgba(0,0,0,0.2)"
            height="200"
            class="align-end white--text"
          >
            <v-card-title>Settings</v-card-title>
          </v-img>
          <v-card-text>
            <v-list>
              <v-subheader>POS Modes</v-subheader>
              <v-list-item-group v-model="selectedMode" color="primary">
                <v-list-item
                  v-for="mode in modes"
                  :key="mode"
                  >

                  <v-list-item-content>
                    <v-list-item-title>{{ mode }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
            </v-list>
            <v-divider></v-divider>
            <v-list>
              <v-subheader>Select Reader</v-subheader>
              <v-list-item>
                <v-list-item-content>
                  <reader-selector :readers="readers" @change="setReader"/>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <reader-status :reader-id="readerId" @success="readerSuccess" />
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
          <v-card-actions></v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>


<script>
import RestaurantPOS from '~/components/terminal/RestaurantPOS.vue';
import CoffeeSubscriptionPOS from '~/components/terminal/CoffeeSubscriptionPOS.vue';
import ReaderSelector from '~/components/terminal/ReaderSelector.vue';
import ReaderStatus from '~/components/terminal/ReaderStatus.vue';

export default {
  name: "POSIntegration",
  components: {RestaurantPOS, CoffeeSubscriptionPOS, ReaderSelector, ReaderStatus},
  async asyncData({$axios}){
    const {data: readers} = await $axios.$get('/terminals/', {
        params: {expand: ['data.location']}
      }
    )
    return { readers }
  },
  data: () => ({
    selectedMode:  0,
    modes: ["Restaurant","Coffee Subscription"],
    posConfig: {
      "Restaurant":{
        cardImage: "https://images.pexels.com/photos/735869/pexels-photo-735869.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        cardTitle: "Restaurant POS",
        component: "RestaurantPOS"
      },
      "Coffee Subscription": {
        cardImage: "https://images.pexels.com/photos/894695/pexels-photo-894695.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        cardTitle: "Coffee Subscription",
        component: "CoffeeSubscriptionPOS"
      }
    },
    reader: null
  }),

  computed: {
    config() {
      return this.posConfig[this.modes[this.selectedMode]]
    },
    readerId() {
      if (this.reader) {
        return this.reader.id
      } else {
        return null
      }
    }
  },
  methods: {
    setReader(reader) {
      this.reader = reader
    },
    readerSuccess() {

    }
  }
}
</script>

