<template>
  <v-row justify="center" align="center" class="full-height">
    <v-col cols="12" sm="12" md="10" lg="8">
      <v-card>
        <v-img
          src="https://images.pexels.com/photos/10874555/pexels-photo-10874555.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
          height="300px"
          class="white--text align-end"
          gradient="to top, rgba(0,0,0,0.5), rgba(0,0,0,0.2)"
        >
          <v-card-title>
            Ad Hoc API Queries
          </v-card-title>
          <v-card-subtitle>
            Use the inputs below to make ad hoc Stripe API queries and view the results
          </v-card-subtitle>
        </v-img>
        <v-card-text>
          <v-card-subtitle>Select an API and what action you wish to take</v-card-subtitle>
          <v-row>
            <v-col cols="12" sm="6">
              <api-selector></api-selector>
            </v-col>
            <v-col cols="12" sm="6">
              <action-selector></action-selector>
            </v-col>
          </v-row>
          <v-row>
            <ParamForm :params="params"></ParamForm>
          </v-row>

        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import ActionSelector from '~/components/adhoc/ActionSelector.vue'
import ApiSelector from '~/components/adhoc/ApiSelector.vue'
import ParamForm from '~/components/stripe/primitives/ParamForm.vue';
export default {
  name: 'AdHoc',
  components: { ActionSelector, ApiSelector, ParamForm },
  data: () => ({
    params: [
      {type: "boolean", label: "Test1"}
    ]
  })

}
</script>

<style>
.full-height {
  height: 100%;
}
</style>
