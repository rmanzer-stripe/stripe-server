<template>
  <v-container fluid>
    <v-row align="center">
      <v-col cols="12" sm="12">
        <v-select
        v-model="choice"
        :items="actions"
        item-text="name"
        item-value="name"
        return-object
        single-line
        label="Select API Action"
      ></v-select>
      </v-col>
      <v-col cols="12" sm="12">
        <v-text-field
        v-if="needId"
        v-model="id"
        label="ID"
        :rules="[checkId]"
        transition="v-fade-transition"
        ></v-text-field>
       </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data: () =>({
    choice: null,
    id: '',
    actions: [
      {name: 'Get', detail: true},
      {name: 'Create', detail: false},
      {name: 'Update', detail: true},
      {name: 'Delete', detail: true},
      {name: 'List', detail: false}
    ]
  }),
  computed: {
    needId() {
      return this.choice !== null && this.choice.detail
    }
  },
  methods: {
    checkId() {
      return this.needId && this.id.length !== 0 || 'ID is required for this action'
    }
  }
}
</script>
