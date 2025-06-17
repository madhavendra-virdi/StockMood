<template>
  <el-dialog class="global-window" :title="title" status-icon :visible="visible" :width="width"
    :close-on-click-modal="false" :close-on-press-escape="false" @close="close">
    <div class="body">
      <slot></slot>
    </div>
    <div slot="footer" class="window__footer">
      <el-button @click="confirm" :loading="confirmWorking" type="primary">确定</el-button>
      <el-button @click="close">Cancel</el-button>
    </div>
  </el-dialog>
</template>

<script>
export default {
  name: 'GlobalWindow',
  props: {
    width: {
      type: String,
      default: '36%'
    },
    // Confirm the loading status of the button
    confirmWorking: {
      type: Boolean,
      default: false
    },
    // title
    title: {
      type: String,
      default: ''
    },
    // Show or not
    visible: {
      type: Boolean,
      required: true
    }
  },
  methods: {
    confirm() {
      this.$emit('confirm')
    },
    close() {
      this.$emit('update:visible', false)
    }
  }
}
</script>

<style scoped lang="less">
@import "../../assets/style/variable";
// Input height
@input-height: 32px;

.global-window {

  // header
  /deep/ .el-dialog__header {
    border-bottom: 1px solid #eee;
  }

  // Content section
  /deep/ .el-dialog__body {
    // form
    .el-form-item {
      margin-bottom: 18px;

      &:last-of-type {
        margin-bottom: 0;
      }

      .el-form-item__content>* {
        width: 100%;
      }
    }
  }

  // Tail button
  .el-dialog__footer {
    .el-button {
      height: @input-height;
      width: 76px;
      padding: 0;
    }
  }
}
</style>
