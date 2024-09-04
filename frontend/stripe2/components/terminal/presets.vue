<template>
  <v-row>
    <v-col cols="12" md="6" v-for="(product, i) in presets" :key="i">
      <CoreProductCard :product="product" @click="EmitPrice" />
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'TerminalChargePresets',
  data: () => ({
    presets: [
      {
        image_url: 'https://images.pexels.com/photos/1753050/pexels-photo-1753050.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
        name: 'Avocado',
        price: 1200,
        description: 'A tasty source of omega-3s and happiness'
      }, {
       image_url: "https://images.pexels.com/photos/1093038/pexels-photo-1093038.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
       name: "Bananas",
       price: 3400,
       description: 'A healthy and natural source of potassium as well as fiber.'
      }, {
        image_url: 'https://images.pexels.com/photos/7263032/pexels-photo-7263032.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
        name: 'Toothbrush',
        price: 500,
        description: "Sometimes you just need a toothbrush, you know?"
      }
    ]
  }),
  methods: {
    LogClick(e) {
      console.log(e);
    },
    EmitPrice(e) {
      this.$emit('click', e)
    }
  }
}
</script>

<style>

</style>
