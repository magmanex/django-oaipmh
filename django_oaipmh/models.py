"""Models for exposing OAI-PMH harvestable metadata from objects."""

from itertools import chain

from django.db.models import Manager

from django_oaipmh.exceptions import CannotDisseminateFormat, IDDoesNotExist


class OAIItemManager(Manager):
    """Manager that can aggregate :class:`OAIItem` s."""
    
    def all(self):
        """Returns an iterable chain object of all :class:`OAIItem` s in the
        repository.
        """
        return chain(*[model.get_oai_queryset() for model in OAIItem.__subclasses__()])

    def get(self, identifier):
            """Returns a single item by its identifier."""
            for item in self.all():
                if item.oai_identifier() == identifier:
                    return item
            raise IDDoesNotExist('No item found for identifier: {}.'.format(identifier))


class OAIItem(object):
    """Interface used to indicate that a given subclass is an OAI item and can
    expose its metadata for harvest via an :class:`django_oaipmh.views.OAIProvider`.

    N.B. none of these methods are meant to be called directly on OAIItem - 
    only on a subclass or instance.

    Example: calling OAIItem.objects.all() will use the OAIItemManager to call
    get_oai_queryset on all subclasses of OAIItem where it should be defined; 
    we'll never call OAIItem.get_oai_queryset directly.
    """

    objects = OAIItemManager()

    @classmethod
    def get_oai_queryset(cls):
        """Should return an iterable comprising the set of all :class:`OAIItem`
        s of the given class. Doesn't need to be a :django:class:`QuerySet`.
        """
        raise NotImplementedError

    def get_oai_record(self, metadata_prefix):
        """Retrieve an XML metadata object for the item in a specified format.
        Requires a method of the form get_oai_record_[format] to be implemented
        for each format.
        """
        try:
            return getattr(self, 'get_oai_record_{}'.format(metadata_prefix))()
        except AttributeError:
            raise CannotDisseminateFormat('Item doesn\'t support format \'%s\'.'
                                          % metadata_prefix)

    def oai_identifier(self):
        """Override to return a unique identifier for the item. See the `OAI
        guidelines <ttp://www.openarchives.org/OAI/2.0/guidelines-oai-identifier.htm>`_
        for more information on identifier formats.
        """
        raise NotImplementedError

    def oai_datestamp(self):
        """Override to return a modification date/timestamp. Supported formats
        are ``YYYY-MM-DD``, ``YYYY-MM-DDThh:mm:ssZ``. Should match the granularity
        specified by the :class:`django_oaipmh.views.OAIProvider` that will
        expose this item.
        """
        raise NotImplementedError

    def oai_sets(self):
        """Override to return an iterable of :class:`OAISet` (s) that the item
        belongs to.
        """
        return []


class OAISet():
    """Interface used to indicate that a given subclass is an OAI set and can
    expose its metadata for harvest via an
    :class:`django_oaipmh.views.OAIProvider`.
    """
    

    @classmethod
    def get_oai_queryset(cls):
        """Should return an iterable comprising the set of all :class:`OAISets`
        s of the given class. Doesn't need to be a :django:class:`QuerySet`.
        """
        raise NotImplementedError

    def oai_sets(self):
        """Override to return an iterable of :class:`OAISet` (s) that the set
        belongs to.
        """
        raise NotImplementedError

    def oai_items(self):
        """Override to return an iterable of this set's :class:`OAIItem` s."""
        raise NotImplementedError
