<template>
  <v-container>
    <v-card>
      <v-img
        src="https://images.pexels.com/photos/127027/pexels-photo-127027.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
        gradient="to bottom, rgba(0,0,0,0.1), rgba(0,0,0,0.5)"
        height="500"
        class="align-end white--text"
      >
        <v-card-title class="text-h4">
          We are very sad to see you go
        </v-card-title>
        <v-card-subtitle class="text-h6">
          Like, really sad.  Why would you do that to us?
        </v-card-subtitle>
      </v-img>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'CancelAction'
}
</script>
