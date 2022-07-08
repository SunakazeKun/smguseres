import pyjmap
import pyjkernel
import os

__all__ = ["UseResourceGenerator"]

__ARCHIVE_MARKER__ = "ARCHIVE "                      # Marks the starting of an archive path in a logged line
__SOUND_MARKER__ = "SOUND "                          # Marks the starting of a sound name in a logged line
__HASH_TABLE__ = pyjmap.SuperMarioGalaxyHashTable()  # Hash lookup table for BCSV field names

__LOCALIZE_PATHS__ = [
    "/LocalizeData/JpJapanese", "/LocalizeData/UsEnglish", "/LocalizeData/UsSpanish", "/LocalizeData/UsFrench",
    "/LocalizeData/EuEnglish", "/LocalizeData/EuSpanish", "/LocalizeData/EuFrench", "/LocalizeData/EuGerman",
    "/LocalizeData/EuItalian", "/LocalizeData/EuDutch", "/LocalizeData/CnSimpChinese", "/LocalizeData/CnTradChinese",
    "/LocalizeData/KrKorean", "/LocalizeData/AsTradChinese"
]


def __strip_localize_path__(archive_path):
    for locale in __LOCALIZE_PATHS__:
        if archive_path.startswith(locale):
            return archive_path.replace(locale, "")
    return archive_path


class UseResourceGenerator:
    def __init__(self, game_files: str, galaxy_name: str, scenarios: int):
        """
        Sets up a new generator for the specified galaxy and its main scenarios (any scenario with PowerStarType set to
        Normal). This also prepares all storages and the RARC archive for later use.

        :param game_files: the path containing the game's contents.
        :param galaxy_name: the galaxy's name.
        :param scenarios: the number of main scenarios.
        """
        self._game_files_ = game_files
        self._galaxy_name_ = galaxy_name
        self._scenarios_ = scenarios

        # Prepare working storage
        self._scenario_archives_ = [list() for _ in range(scenarios + 1)]
        self._scenario_sounds_ = [list() for _ in range(scenarios + 1)]

        # Prepare UseResource archive
        self._archive_ = pyjkernel.create_new_archive("Stage")
        self._archive_.create_folder("Stage/csv")
        self._archive_.create_file("Stage/csv/common.bcsv")

        for i in range(1, scenarios + 1):
            self._archive_.create_file(f"Stage/csv/scenario_{i}.bcsv")

        self._archive_.create_file("Stage/csv/sound_common.bcsv")

        for i in range(1, scenarios + 1):
            self._archive_.create_file(f"Stage/csv/sound_scenario_{i}.bcsv")

    def __repr__(self):
        return f"{self._galaxy_name_} UseResource Generator"

    @property
    def game_files(self):
        """The path containing the game's contents."""
        return self._game_files_

    @property
    def galaxy_name(self):
        """The galaxy's name."""
        return self._galaxy_name_

    @property
    def scenarios(self):
        """The number of main scenarios."""
        return self._scenarios_

    def write_analyzed(self):
        """Builds the entire UseResource archive using the generated Dolphin logs."""
        all_archives = list()
        all_sounds = list()

        # 1 -- Read text dumps
        for i in range(1, self._scenarios_ + 1):
            file_path = os.path.join(self._game_files_, f"UseResourceLogs/{self._galaxy_name_}_Scenario{i}.txt")
            archives = self._scenario_archives_[i]
            sounds = self._scenario_sounds_[i]

            with open(file_path, "r") as f:
                for l in f.readlines():
                    l = l.strip("\r\n")

                    if __ARCHIVE_MARKER__ in l:
                        arc = l[l.index(__ARCHIVE_MARKER__) + len(__ARCHIVE_MARKER__):]
                        arc = __strip_localize_path__(arc)

                        if arc not in archives:
                            archives.append(arc)
                        if arc not in all_archives:
                            all_archives.append(arc)
                    elif __SOUND_MARKER__ in l:
                        snd = l[l.index(__SOUND_MARKER__) + len(__SOUND_MARKER__):]

                        if snd not in sounds:
                            sounds.append(snd)
                        if snd not in all_sounds:
                            all_sounds.append(snd)

        # 2 -- Collect common resources
        common_archives = self._scenario_archives_[0]
        common_sounds = self._scenario_sounds_[0]

        for arc in all_archives:
            is_common = True

            for archives in self._scenario_archives_[1:]:
                if arc not in archives:
                    is_common = False
                    break

            if is_common:
                common_archives.append(arc)

        for snd in all_sounds:
            is_common = True

            for sounds in self._scenario_sounds_[1:]:
                if snd not in sounds:
                    is_common = False
                    break

            if is_common:
                common_sounds.append(snd)

        # 3 -- Remove common resources from scenarios
        for arc in common_archives:
            for archives in self._scenario_archives_[1:]:
                if arc in archives:
                    archives.remove(arc)

        for snd in common_sounds:
            for sounds in self._scenario_sounds_[1:]:
                if snd in sounds:
                    sounds.remove(snd)

        # 4 -- Write BCSV files
        def write_bcsv(resources: list, file: str, field: str):
            bcsv = pyjmap.JMapInfo(__HASH_TABLE__)
            bcsv.create_field(field, pyjmap.JMapFieldType.STRING_OFFSET, "<Anonymous>")

            for r in resources:
                bcsv.create_entry()[field] = r

            self._archive_.get_file(f"Stage/csv/{file}.bcsv").data = pyjmap.pack_buffer(bcsv)

        for i in range(self._scenarios_ + 1):
            archives = self._scenario_archives_[i]
            sounds = self._scenario_sounds_[i]

            write_bcsv(archives, "common" if i == 0 else f"scenario_{i}", "ResourceName")
            write_bcsv(sounds, "sound_common" if i == 0 else f"sound_scenario_{i}", "SoundName")

        arc_path = os.path.join(self._game_files_, f"StageData/{self._galaxy_name_}/{self._galaxy_name_}UseResource.arc")
        pyjkernel.write_archive_file(self._archive_, arc_path, compression=pyjkernel.JKRCompression.SZS)

    def write_dummy(self):
        """Creates and stores an empty UseResource archive for the galaxy."""
        arc = pyjkernel.create_new_archive("Stage")
        arc.create_folder("Stage/csv")

        arc_path = os.path.join(self._game_files_, f"StageData/{self._galaxy_name_}/{self._galaxy_name_}UseResource.arc")
        pyjkernel.write_archive_file(arc, arc_path, compression=pyjkernel.JKRCompression.SZS)
