<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="6" sm="12">
        <CreateTestClock />
      </v-col>
      <v-col cols="12" md="6" sm="12">
        <CreateCustomer />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import CreateCustomer from '~/components/stripe/CreateCustomer.vue';
import CreateTestClock from '~/components/stripe/CreateTestClock.vue';

export default {
    components: { CreateCustomer, CreateTestClock },
    head: {
      title: "Test Clock Integration"
    }
}
</script>
