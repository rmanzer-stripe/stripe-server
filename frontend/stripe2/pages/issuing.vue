<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="12" md="10">
      <v-card>
        <v-img
        class="white--text align-end"
        src="https://images.pexels.com/photos/583881/pexels-photo-583881.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
        height="300"
        gradient="to top, rgba(0,0,0, 0.6), rgba(0,0,0,0.3)"
        >
          <v-card-title class="text-h2">Card Issuing</v-card-title>
        </v-img>
      </v-card>
    </v-col>
    <v-col cols="12" md="10">
      <v-card>
        <v-card-title>
          Issuing Actions
        </v-card-title>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'IssuingHome',
}
</script>
