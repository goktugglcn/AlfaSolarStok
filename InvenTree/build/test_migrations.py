"""Tests for the build model database migrations."""

from django_test_migrations.contrib.unittest_case import MigratorTestCase

from InvenTree import unit_test


class TestForwardMigrations(MigratorTestCase):
    """Test entire schema migration sequence for the build app."""

    migrate_from = ('build', unit_test.getOldestMigrationFile('build'))
    migrate_to = ('build', unit_test.getNewestMigrationFile('build'))

    def prepare(self):
        """Create initial data!"""
        Part = self.old_state.apps.get_model('part', 'part')

        buildable_part = Part.objects.create(
            name='Widget',
            description='Buildable Part',
            active=True,
        )

        with self.assertRaises(TypeError):
            # Cannot set the 'assembly' field as it hasn't been added to the db schema
            Part.objects.create(
                name='Blorb',
                description='ABCDE',
                assembly=True
            )

        Build = self.old_state.apps.get_model('build', 'build')

        Build.objects.create(
            part=buildable_part,
            title='A build of some stuff',
            quantity=50
        )

    def test_items_exist(self):
        """Test to ensure that the 'assembly' field is correctly configured"""
        Part = self.new_state.apps.get_model('part', 'part')

        self.assertEqual(Part.objects.count(), 1)

        Build = self.new_state.apps.get_model('build', 'build')

        self.assertEqual(Build.objects.count(), 1)

        # Check that the part object now has an assembly field
        part = Part.objects.all().first()
        part.assembly = True
        part.save()
        part.assembly = False
        part.save()


class TestReferenceMigration(MigratorTestCase):
    """Test custom migration which adds 'reference' field to Build model."""

    migrate_from = ('build', unit_test.getOldestMigrationFile('build'))
    migrate_to = ('build', '0018_build_reference')

    def prepare(self):
        """Create some builds."""
        Part = self.old_state.apps.get_model('part', 'part')

        part = Part.objects.create(
            name='Part',
            description='A test part'
        )

        Build = self.old_state.apps.get_model('build', 'build')

        Build.objects.create(
            part=part,
            title='My very first build',
            quantity=10
        )

        Build.objects.create(
            part=part,
            title='My very second build',
            quantity=10
        )

        Build.objects.create(
            part=part,
            title='My very third build',
            quantity=10
        )

        # Ensure that the builds *do not* have a 'reference' field
        for build in Build.objects.all():
            with self.assertRaises(AttributeError):
                print(build.reference)

    def test_build_reference(self):
        """Test that the build reference is correctly assigned to the PK of the Build"""
        Build = self.new_state.apps.get_model('build', 'build')

        self.assertEqual(Build.objects.count(), 3)

        # Check that the build reference is properly assigned
        for build in Build.objects.all():
            self.assertEqual(str(build.reference), str(build.pk))


class TestReferencePatternMigration(MigratorTestCase):
    """Unit test for data migration which converts reference to new format.

    Ref: https://github.com/inventree/InvenTree/pull/3267
    """

    migrate_from = ('build', '0019_auto_20201019_1302')
    migrate_to = ('build', unit_test.getNewestMigrationFile('build'))

    def prepare(self):
        """Create some initial data prior to migration"""

        Setting = self.old_state.apps.get_model('common', 'inventreesetting')

        # Create a custom existing prefix so we can confirm the operation is working
        Setting.objects.create(
            key='BUILDORDER_REFERENCE_PREFIX',
            value='BuildOrder-',
        )

        Part = self.old_state.apps.get_model('part', 'part')

        assembly = Part.objects.create(
            name='Assy 1',
            description='An assembly',
            level=0, lft=0, rght=0, tree_id=0,
        )

        Build = self.old_state.apps.get_model('build', 'build')

        for idx in range(1, 11):
            Build.objects.create(
                part=assembly,
                title=f"Build {idx}",
                quantity=idx,
                reference=f"{idx + 100}",
                level=0, lft=0, rght=0, tree_id=0,
            )

    def test_reference_migration(self):
        """Test that the reference fields have been correctly updated"""

        Build = self.new_state.apps.get_model('build', 'build')

        for build in Build.objects.all():
            self.assertTrue(build.reference.startswith('BuildOrder-'))

        Setting = self.new_state.apps.get_model('common', 'inventreesetting')

        pattern = Setting.objects.get(key='BUILDORDER_REFERENCE_PATTERN')

        self.assertEqual(pattern.value, 'BuildOrder-{ref:04d}')
