from scrapy.contrib.downloadermiddleware.defaultheaders import DefaultHeadersMiddleware

__author__ = 'barbossa'


class MyHeadersMiddleware(DefaultHeadersMiddleware):
    """
    def process_request(request, spider):
        This method is called for each request that goes through the download middleware
        process_request() should either: return None, return a Response object, return a Request object, or raise IgnoreRequest
        If it returns None, Scrapy will continue processing this request, executing all other middlewares until,
        finally, the appropriate downloader handler is called the request performed (and its response downloaded)
        If it returns a Response object, Scrapy won't bother calling any other process_request() or
        process_exception() methods, or the appropriate download function; it'll return that response
        The process_response() methods of installed middleware is always called on every response
        If it returns a Request object, Scrapy will stop calling process_request methods and reschedule the
        returned request Once the newly returned request is performed, the appropriate middleware chain will be
        called on the downloaded response
        If it raises an IgnoreRequest exception, the process_exception() methods of installed down-
        loader middleware will be called If none of them handle the exception, the errback function of the request
        (Requesterrback) is called If no code handles the raised exception, it is ignored and not logged
        (unlike other exceptions)
        Parameters
        @param request (Request object)  the request being processed
         spider (BaseSpider object)  the spider for which this request is intended

    def process_response(request, response, spider):
        process_response() should either: return a Response object, return a Request object or raise a
        IgnoreRequest exception
        If it returns a Response (it could be the same given response, or a brand-new one), that response will
        continue to be processed with the process_response() of the next middleware in the chain
        If it returns a Request object, the middleware chain is halted and the returned request is resched-
        uled to be downloaded in the future This is the same behavior as if a request is returned from
        process_request()
        If it raises an IgnoreRequest exception, the errback function of the request (Requesterrback) is
        called If no code handles the raised exception, it is ignored and not logged (unlike other exceptions)
        Parameters
         request (is a Request object)  the request that originated the response
         response (Response object)  the response being processed
         spider (BaseSpider object)  the spider for which this response is intended

    def process_exception(request, exception, spider):
        Scrapy calls process_exception() when a download handler or a process_request() (from a
        downloader middleware) raises an exception (including an IgnoreRequest exception)
        process_exception() should return: either None, a Response object, or a Request object
        If it returns None, Scrapy will continue processing this exception, executing any other
        process_exception() methods of installed middleware, until no middleware is left and the default
        Scrapy calls process_exception() when a download handler or a process_request() (from a
        downloader middleware) raises an exception (including an IgnoreRequest exception)
        process_exception() should return: either None, a Response object, or a Request object
        If it returns None, Scrapy will continue processing this exception, executing any other
        process_exception() methods of installed middleware, until no middleware is left and the default
        exception handling kicks in
        If it returns a Response object, the process_response() method chain of installed middleware is
        started, and Scrapy won't bother calling any other process_exception() methods of middleware
        If it returns a Request object, the returned request is rescheduled to be downloaded in the future This
        stops the execution of process_exception() methods of the middleware the same as returning a
        response would
        Parameters
         request (is a Request object)  the request that generated the exception
         exception (an Exception object)  the raised exception
         spider (BaseSpider object)  the spider for which this request is intended

    """
    def __init__(self, headers, *args, **kwargs):
        super(MyHeadersMiddleware, self).__init__(headers)
