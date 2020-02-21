import sys, json, boto3

def handler(event,context):
  vote = ''
  
  responseHeaders = {
    'Content-Type': 'text/plain',
    'Access-Control-Allow-Origin': '*'
  }

  try:
    body = json.loads(event['body'])
    vote = body['Vote']
  except:
    e = sys.exc_info()
    
    return {
      'body': 'Invalid payload {0}\nError decoding JSON: {1}'.format(event['body'], str(e)),
      'headers': responseHeaders,
      'statusCode': 500
    }
    
  try:
    # Get the service resource
    sqs = boto3.resource('sqs')
    
    # Get the queue
    queue = sqs.get_queue_by_name(QueueName='decoupled-sqs-application-voting-queue')
    
    messageBody = '{{"Vote": "{0}"}}'.format(vote)
    
    # Create a new message
    response = queue.send_message(MessageBody=messageBody)
    
    # The response is NOT a resource, but gives you a message ID and MD5
    messageId = response.get('MessageId')
  except Exception as e:
    print(e)
    
    return {
      'body': 'Error sending queue message: {0}'.format(str(e)),
      'headers': responseHeaders,
      'statusCode': 500
    }
  
  return {
    'body': '{0}'.format(messageId),
    'headers': responseHeaders,
    'statusCode': 200
  }
  