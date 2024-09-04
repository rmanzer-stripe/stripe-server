<template>
  <v-app >
    <v-navigation-drawer
      v-model="drawer"
      :mini-variant="miniVariant"
      :clipped="clipped"
      fixed
      app
    >

      <nav-list :links="items" :mini="miniVariant"/>
    </v-navigation-drawer>
    <!-- <v-navigation-drawer
      v-model="rightDrawer"
      :mini-variant="miniVariant"
      temporary
      fixed
      app
      right
      >
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="text-h6">Integrations</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>
      <nav-list :links="moreLinks" />
    </v-navigation-drawer> -->
    <v-app-bar :clipped-left="clipped" fixed app>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-btn icon @click.stop="miniVariant = !miniVariant">
        <v-icon>mdi-{{ `chevron-${miniVariant ? 'right' : 'left'}` }}</v-icon>
      </v-btn>
      <v-toolbar-title>{{ title }}</v-toolbar-title>
      <v-spacer></v-spacer>
      
      <div style="max-width: 450px;">
        <account-switcher  />
      </div>
    </v-app-bar>
    <v-main>
      <v-container fluid>
        <Nuxt />
      </v-container>
    </v-main>
    <v-footer :absolute="!fixed" app>
      <span>&copy; C. Ryan Manzer OBO Stripe 2023</span>
    </v-footer>
  </v-app>
</template>

<script>
import NavList from '~/components/nav/NavList.vue';
import AccountSwitcher from '~/components/stripe/AccountSwitcher.vue';


export default {
  name: 'DefaultLayout',
  components: {   NavList, AccountSwitcher },
  data() {
    return {
      clipped: true,
      drawer: false,
      fixed: false,
      sheet: false,
      items: [
        {
          icon: 'mdi-home',
          title: 'Home',
          to: {name: 'index'}
        },
        {
          icon: 'mdi-file-document-check-outline',
          title: "Canonical Integrations",
          to: {name: "CanonicalIntegrations"}
        },
        {
          icon: 'mdi-console-line',
          title: 'Terminal',
          // to: {name: "terminal"}
          children: [
            {
              icon: 'mdi-language-javascript',
              title: 'JS Integration',
              to: { name: "terminal-JsIntegration"}
            },
            {
              icon: 'mdi-server',
              title: 'Server Integration',
              to: { name: "terminal-ServerIntegration"}
            },
            {
              icon: 'mdi-network-pos',
              title: "POS Integration",
              to: {name: "terminal-POSIntegration"}
            }
          ]
        },
        {
          icon: 'mdi-repeat-variant',
          title: 'Subscriptions',
          children: [
            {
              icon: 'mdi-cash-clock',
              title: 'Test Clock',
              to: {name: 'subscriptions-test_clocks'}
            },
            {
              icon: 'mdi-calendar-arrow-right',
              title: "Schedules",
              to: {name: "subscriptions-schedules"}
            }
          ]
        },
        {
          icon: 'mdi-clock',
          title: "Deferred & 2 Step Confirmation",
          to: {name: 'multiStep'}
        },
        {
          icon: 'mdi-credit-card-check-outline',
          title: 'Payment Element Flavors',
          to: {name: 'PaymentElementFlavors'}
        },
         {
          icon: 'mdi-shuffle',
          title: 'Random Integrations',
          to: {name: 'RandomIntegrations'}
         },
         {
          icon: 'mdi-invoice-text-fast-outline',
          title: "Stripe Billing",
          to: {name: 'Billing'}
         },
         {
           icon: 'mdi-cart',
           title: 'Orders API',
           to: {name: 'orders'},
           deprecated: true
        },
         {
          icon: 'mdi-apps-box',
          title: 'Stripe Apps Demo',
          to: {name: 'StripeApp'}
         },
         {
          icon: 'mdi-transit-connection',
          title: "Stripe Connect",
          to: {name: 'Connect'}
         },
         {
          icon: 'mdi-flag-outline',
          title: "India Payments",
          to: {name:'IndiaPayments'}
         },
         {
          ico: 'mdi-handshake',
          title: 'Supermanzer LLC',
          to: {name: 'Supermanzer'}
         }
      ],
      miniVariant: false,
      title: 'Manzer Stripe Integration',
      rightDrawer: false
    }
  },
  head: {
    title: 'Home',
  },
  computed: {
    moreLinks() {
      return this.$store.state.extra_nav_links
    }
  },
  methods: {
    async getResources() {
      const resources = await this.$http.$get('');
      for (const prop in resources) {
        this.items.push({
          icon: 'mdi-link',
          title: prop.charAt(0).toUpperCase() + prop.slice(1),
          to: `${prop}`
        })
      }
    }
  },

}
</script>

<style scoped>
main.v-main {
  background-image: linear-gradient(to top, #f3e7e9 0%, #e3eeff 99%, #e3eeff 100%);
}
</style>
