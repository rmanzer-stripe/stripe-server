<template>
  <v-form>
    <v-container>
      <v-row>
        <v-col cols="12" sm="12" md="4">
          <component
            :is="getPrimitive(param.type)"
            v-for="param, i in params"
            :key="i"
            :ref="`primitive_${i}`"
            :label="getParam(param, 'label')"
            :hint="getParam(param, 'hint')"
            :rules="getParam(param, 'rules')"
            :items="getParam(param, 'items')"
            @changed="logEvent"
            />
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>

<script>

import Boolean from './boolean.vue';
import Enum from './enum.vue';
import Integer from './integer.vue';
import String from './string.vue';

export default {
  props: {
    params: {type: Array, required: false, default: () => []}
  },
  data: () => ({
    primitives: {
      'string': String,
      'integer': Integer,
      'enum': Enum,
      'boolean': Boolean
    },
    defaults: {
      rules: [],
      label: null,
      hint: null,
      items: [],
      color: null
    }
  }),
  methods: {
    getPrimitive(type) {
      return this.primitives[type]
    },
    getParam(paramObj, paramKey) {
      return paramObj[paramKey] ? paramObj[paramKey] : this.getDefault(paramKey)
    },
    getDefault(key) {
      return this.defaults[key]
    },
    logEvent(ev) {
      console.log(ev);
    }
  }
}
</script>
