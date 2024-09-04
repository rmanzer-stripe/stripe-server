<template>
  <div>
    <v-img
      :src="img_src"
      :max-height="img_height"
      :gradient="img_gradient"
      :class="classString"
      :position="position"

    >
      <v-card-title v-text="title_text"></v-card-title>
    </v-img>
  </div>
</template>

<script>
export default {
  props: {
    img_src: { type: String, required: false, default: '' },
    img_gradient: { type: String, required: false, default: '' },
    img_height: {type: Number, required: false, default: 300},
    title_color: { type: String, required: false, default: 'white' },
    title_text: {type: String, required: false, default: ''},
    position: {type: String, required:false, default: 'top center'},
  },
  computed: {
    classString() {
      return `${this.title_color}--text align-end`
    }
  }
}
</script>
