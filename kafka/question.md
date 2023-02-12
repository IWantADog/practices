# question

- [ ] kafka produce的处理是异步的吗
  - produce似乎时异步的
  - 当每次produce之前还需要调用poll方法，调用poll方法会获取发送成功的数据，并且触发注册的回调函数。
- [x] 如果kafka的进程被kill，是否会导致数据的丢失
  - kafka中的produce也有一个flush方法，等待缓存队列中的数据完全处理完毕。